#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from telegram_util import log_on_fail, isInt
from telegram.ext import Updater
import plain_db
import album_sender
import time
import to_album
import pytumblr
from bs4 import BeautifulSoup
import cached_url
from telegram_util import AlbumResult as Result

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

with open('db/setting') as f:
	setting = yaml.load(f, Loader=yaml.FullLoader)

existing = plain_db.loadKeyOnlyDB('existing')
tele = Updater(credential['bot_token'], use_context=True)
debug_group = tele.bot.get_chat(credential['debug_group'])
translate_channel = tele.bot.get_chat(credential['translate_channel'])

client = pytumblr.TumblrRestClient(
    credential['consumer_key'],
    credential['consumer_secret'],
    credential['token'],
    credential['token_secret'],
)

def tryPost(channel, post, sub_setting):
	url = post['post_url']
	if post['note_count'] < 500:
		return
	if existing.contain(url):
		return
	with open('tmp_post', 'w') as f:
		f.write('%s\n\n%s' % (url, str(post)))
	album = to_album.get(post)
	with open('tmp_post', 'w') as f:
		f.write('%s\n\n%s\n\n%s' % (url, str(album), str(post)))
	try:
		album_sender.send_v2(channel, album)
		album_sender.send_v2(translate_channel, album.toPlain())
	except Exception as e:
		print('tumblr sending fail', url, e)
		with open('tmp_failed_post', 'w') as f:
			f.write('%s\n\n%s\n\n%s\n\n%s' % (url, str(e), str(album), str(post)))
		return
	existing.add(url)

def getPostIds(soup, sub_setting):
	for url in soup.find_all('a', href=True):
		if 'tumblr' not in url['href']:
			continue
		post_id = url['href'].split('/')[-1]
		if not isInt(post_id):
			continue
		blog_name = url['href'].split('/')[2].split('.')[0]
		yield blog_name, post_id

@log_on_fail(debug_group)
def run():
	sent = False
	for channel_id, channel_setting in setting.items():
		channel = tele.bot.get_chat(channel_id)
		for tag, sub_setting in channel_setting.get('tag', {}).items():
			soup = BeautifulSoup(
				cached_url.get('https://www.tumblr.com/search/' + tag), 'html.parser')
			for blog_name, post_id in getPostIds(soup, sub_setting):
				try:
					post = client.posts(blog_name, id = post_id)['posts'][0]
				except:
					continue
				tryPost(channel, post, sub_setting)
		for people, sub_setting in channel_setting.get('people', {}).items():
			for post in client.posts(people)['posts']:
				tryPost(channel, post, sub_setting)
		
if __name__ == '__main__':
	run()