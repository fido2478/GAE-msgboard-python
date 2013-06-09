import logging
from google.appengine.ext import db
from google.appengine.api import users

POSTS_PER_PAGE = 10

class MessagePost(db.Model):
	def __repr__(self):
		return "user: %s subject: %s body: %s cr_dt: %s" % (self.user, self.subject, self.body, self.cr_dt)

	user = db.StringProperty(required=True)
	subject = db.StringProperty(required=True)
	body = db.TextProperty(required=True)
	cr_dt = db.DateTimeProperty(auto_now_add=True)

class MessageManager(db.Model):
	@staticmethod
	def add(user, subject, body):
		mp = MessagePost(user=user, subject=subject, body=body)
		logging.info(mp)
		mp.put()

	@staticmethod
	def getSummaryList(result_offset):
		global POSTS_PER_PAGE
		posts = []
		q = db.Query(MessagePost)

		q.order('-cr_dt')
		results = q.fetch(
			limit = POSTS_PER_PAGE,
			offset = int(result_offset-1) * POSTS_PER_PAGE)

		for result in results:
			posts.append(result)
		return posts

	@staticmethod		
	def getMessage(msg_id):
		return MessagePost.get_by_id(msg_id)

	@staticmethod
	def getNumberOfPages():
		global POSTS_PER_PAGE
		q = db.Query(MessagePost)
		return 1 + ((q.count()-1) / POSTS_PER_PAGE)
