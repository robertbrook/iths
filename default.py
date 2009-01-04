import os
import feedparser
from operator import itemgetter
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import time 
from datetime import datetime 

def make_datetime(s, fmt='%Y-%m-%d %H:%M'): 
     '''convert string to datetime''' 
     ts = time.mktime(time.strptime(s, fmt)) 
     return datetime.fromtimestamp(ts) 
def inRange(s, ranges): 
     dt = make_datetime(s) 
     for begin,end in ranges: 
         if begin <= dt <= end: 
             return True 
     else: 
         return False 
ranges = [(make_datetime(b), make_datetime(e)) for (b,e) in [ 
     ('2008-12-18 23:59', '2009-01-12 00:00'), 
     # ('2005-06-12 12:30', '2005-06-14 15:30'), 
     ]] 
# print inRange('2005-06-11 12:30', ranges)

class MainPage(webapp.RequestHandler):
  def get(self):
    commons_sitting = 0
    lords_sitting = 0
    commons = get_feed("http://services.parliament.uk/calendar/commons.rss")
    lords = get_feed("http://services.parliament.uk/calendar/lords.rss")
    # bbc = get_feed("http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/uk_politics/rss.xml")
    bbc = get_feed("http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/programmes/bbc_parliament/rss.xml")

    if commons.entries: commons_sitting = 1
    if lords.entries: lords_sitting = 1
    
    template_values = {
      'today': datetime.today().strftime('%Y-%m-%d %H:%M'),
      'inRecess': inRange(datetime.today().strftime('%Y-%m-%d %H:%M'), ranges),
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
