#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'tumblr_to_album'

from telegram_util import AlbumResult as Result
from bs4 import BeautifulSoup

def getImgs(content):
	soup = BeautifulSoup(content, 'html.parser')
	for item in soup.find_all('img'):
		yield item['src']

def getImgsJson(content):
	for photo in content:
		yield photo['original_size']['url']

def get(content):
    result = Result()
    result.url = content['post_url']
    result.video = content.get('video_url')
    result.cap_html_v2 = content['summary'] # may need to add later
    result.imgs = list(getImgsJson(content.get('photos', []))) or list(getImgs(content['body']))
    return result