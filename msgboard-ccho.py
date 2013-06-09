# -*- coding: utf-8 -*-
import logging
import webapp2
import datetime
import os
from message import MessagePost, MessageManager
from google.appengine.ext.webapp.template import render

class MessageBoardHandler(webapp2.RequestHandler):
	def get(self):
		self.redirect("/list/1")

class ListPostsHandlerDefault(webapp2.RequestHandler):
	def get(self):
			self.redirect("/list/1")

class ListPostsHandler(webapp2.RequestHandler):
	def get(self, page_no):
		try:
			p = int(page_no)
			logging.info(xrange(1,MessageManager.getNumberOfPages()))

			context = {
				'msg_posts': MessageManager.getSummaryList(p),
				'page_range': xrange(1,MessageManager.getNumberOfPages()+1) #+1 due to for loop behavior in Django 
			}

			tpl = os.path.join(os.path.dirname(__file__), 'templates/add_message.html')
			self.response.out.write(render(tpl, context))

		except (TypeError, ValueError):
			self.error(500)	

class ViewPostHandler(webapp2.RequestHandler):
	def get(self, post_no):
		try:
			post = MessageManager.getMessage(long(post_no))
			context = {
				'msg_post': post
			}
			tpl = os.path.join(os.path.dirname(__file__), 'templates/view_message.html')
			self.response.out.write(render(tpl, context))

		except (TypeError, ValueError):
			self.error(500)

class AddPostHandler(webapp2.RequestHandler):
	def post(self):
		try:
			MessageManager.add(
				self.request.get("author", default_value="unspecified"),
				self.request.get("subject", default_value="no subject"),
				self.request.get("message_body", default_value="nt"))

			self.redirect("/list")

		except (TypeError, ValueError):
			self.error(500)


app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MessageBoardHandler, name='main', methods=['GET']),
	webapp2.Route(r'/list', handler=ListPostsHandlerDefault, name='listmessagedefault', methods=['GET']),
	webapp2.Route(r'/list/<page_no:\d*>', handler=ListPostsHandler, name='listmessages', methods=['GET']),
	webapp2.Route(r'/view/<post_no:\d*>', handler=ViewPostHandler, name='viewmessage', methods=['GET']),
	webapp2.Route(r'/add', handler=AddPostHandler, name='addmessage', methods=['POST']), 
])


""" 
def main():
	app.run()

if __name__ == '__main__':
	main()
"""

