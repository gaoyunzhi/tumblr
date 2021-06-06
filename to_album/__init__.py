#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'tumblr_to_album'

from telegram_util import AlbumResult as Result

def dedup(images):
	exist = set()
	for image in images:
		if image in exist:
			continue
		if 'p32x32' in image:
			continue
		exist.add(image)
		yield image

def getText(text, comment, link):
	if link:
		return text + '\n\n' + link
	if not comment or text == comment:
		return text
	index = comment.find('\n\n')
	if index == -1:
		return text
	comment = comment[index:].strip()
	if len(comment) < 10:
		return text
	if not text:
		return comment
	return text + '\n\ncomment: ' + comment

def get(content):
    result = Result()
    result.url = content['post_url']
    result.video = content.get('video_url')
    result.cap_html_v2 = content['summary'] # may need to add later
    # result.imgs = list(dedup(content['images'] or [])) # todo
    return result