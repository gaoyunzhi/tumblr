#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'tumblr_to_album'

from telegram_util import AlbumResult as Result
from bs4 import BeautifulSoup
from tumdlr import downloader
import cached_url
import os

def getImgs(content):
	soup = BeautifulSoup(content, 'html.parser')
	for item in soup.find_all('img'):
		yield item['src']

def getImgsJson(content):
	for photo in content:
		yield photo['original_size']['url']

def preDownload(img):
	filename = cached_url.getFilePath(img)
	if os.path.exists(filename):
		return
	downloader.download(img, filename, silent=True)

def getText(content):
	soup = BeautifulSoup(content, 'html.parser')
	return soup.getText(separator='\n\n').strip('\u200b').strip()

def get(content):
    result = Result()
    result.url = content['post_url']
    result.video = content.get('video_url')
    result.cap_html_v2 = getText(content.get('caption', '')) or content['summary']
    result.imgs = list(getImgsJson(content.get('photos', []))) or list(getImgs(content.get('body', '')))
    for img in result.imgs:
    	preDownload(img)
    return result