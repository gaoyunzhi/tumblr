from tumblr_collect import *

def testPost(blog_name, post_id):
	post = client.posts(blog_name, id = post_id)['posts'][0]
	with open('tmp_post_test', 'w') as f:
		f.write('%s\n\n%s' % (url, str(post)))

if __name__ == '__main__':
	testPost(649192151716069376)