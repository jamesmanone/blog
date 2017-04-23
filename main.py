import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class BlogPosts(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    timestamp = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.write('TODO!')

class NewPostHandler(Handler):
    def get(self):
        self.render('new.html', pagename='New Post')

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')

        if title and content:
            self.write('Nice one!')
        else:
            error = "You must complete both fields"
            self.render('new.html', error = error, title = title,
                        content = content, pagename = 'New Post')

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/newpost', NewPostHandler)
], debug=True)
