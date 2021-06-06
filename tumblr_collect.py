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

client = pytumblr.TumblrRestClient(
    credential['consumer_key'],
    credential['consumer_secret'],
    credential['token'],
    credential['token_secret'],
)

def tryPost(channel, album):
	if existing.contain(album.url):
		return
	try:
		album_sender.send_v2(channel, album)
	except Exception as e:
		print('tumblr sending fail', album.url, e)
		with open('tmp_failed_post', 'w') as f:
			f.write('%s\n\n%s\n\n%s' % (url, str(e), str(album)))
		return
	existing.add(album.url)

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
				client.posts(blog_name, id = post_id)
				return
		for people, sub_setting in channel_setting.get('people', {}).items():
			for post in client.posts(people):
				tryPost(channel, post, sub_setting)
		# for page, detail in schedule[:1]:
		# 	posts = tumblr_scraper.get_posts(page, pages=10)
		# 	count = 0
		# 	for post in posts:
		# 		count += 1
		# 		url = post['post_url']
		# 		with open('nohup.out', 'a') as f:
		# 			f.write('%s\n%s\n\n' % (url, str(post)))
		# 		if existing.contain(url):
		# 			continue
		# 		if getKey(url) in [getKey(item) for item in existing._db.items.keys()]:
		# 			continue
		# 		# if post['likes'] < detail.get('likes', 100):
		# 		# 	continue
		# 		# album = tumblr_to_album.get(post)
		# 		album_sender.send_v2(channel, album)
		# 		if not sent:
		# 			sent = True
		# 		else:
		# 			item_len = len(album.imgs) or 1
		# 			time.sleep(item_len * item_len + 5 * item_len)
		# 		try:
		# 			album_sender.send_v2(channel, album)
		# 		except Exception as e:
		# 			print('tumblr sending fail', url, e)
		# 			with open('nohup.out', 'a') as f:
		# 				f.write('\n%s %s %s' % (url, str(e), str(post)))
		# 			continue
		# 		existing.add(album.url)
		# 	if count == 0:
		# 		print('tumblr fetch fail', page, count)
		# 		return
		
if __name__ == '__main__':
	run()