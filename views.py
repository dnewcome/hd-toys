from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
	def get(self):
			self.response.out.write("<h1>200 OK</h1>")

app = webapp.WSGIApplication([
  ('/', MainHandler)
], debug=True)