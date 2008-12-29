import os
import feedparser
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    commons_sitting = 0
    lords_sitting = 0
    commons = get_feed("http://services.parliament.uk/calendar/commons.rss")
    lords = get_feed("http://services.parliament.uk/calendar/lords.rss")
    bbc = get_feed("http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/programmes/bbc_parliament/rss.xml")
    
    if commons.entries: commons_sitting = 1
    if lords.entries: lords_sitting = 1
    
    template_values = {
      'commons': commons,
      'lords': lords,
      'bbc': bbc,
      'commons_sitting': commons_sitting,
      'lords_sitting': lords_sitting,
       }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainPage)],debug=True)

def main():
  run_wsgi_app(application)
  
def get_feed(url):
  return feedparser.parse(urlfetch.fetch(url).content)

if __name__ == "__main__":
  main()
