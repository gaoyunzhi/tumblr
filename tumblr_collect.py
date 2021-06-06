#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from telegram_util import log_on_fail
from telegram.ext import Updater
import plain_db
import cached_url
from bs4 import BeautifulSoup
import album_sender
import time
import tumblr_to_album
import pytumblr
import random

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
    credential['oauth_token'],
    credential['oauth_secret'],
)

@log_on_fail(debug_group)
def run():
	sent = False
	for channel_id, channel_setting in setting.items():
		channel = tele.bot.get_chat(channel_id)
		for tag, setting in channel_setting.get('tag', {}).items():
			print(client.tagged(tag))
			return
		for people, setting in channel_setting.get('people', {}).items():
			print(client.posts(people))
			return
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