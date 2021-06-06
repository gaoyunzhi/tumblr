from tumblr_collect import *

def testPost(blog_name, post_id):
	post = client.posts(blog_name, id = post_id)['posts'][0]
	with open('tmp_post_test', 'w') as f:
		f.write(str(post))
	channel = tele.bot.get_chat(420074357)
	album = to_album.get(post)
	album_sender.send_v2(channel, album)

if __name__ == '__main__':
	testPost('liberaljane', 649192151716069376)