import os
import feedparser
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
def inRangeCommons(s, ranges): 
     dt = make_datetime(s) 
     for begin,end in ranges: 
         if begin <= dt <= end: 
             return True 
     else: 
         return False 
ranges = [(make_datetime(b), make_datetime(e)) for (b,e) in [ 
     ('2008-12-18 23:59', '2009-01-12 00:00'), 
     ('2009-02-12 00:00', '2009-02-23 23:59'), 
     ('2009-04-02 00:00', '2009-04-20 23:59'),
     ('2009-05-21 00:00', '2009-06-01 23:59'),
     ('2009-07-21 00:00', '2009-08-12 23:59')
     ]] 
def inRangeLords(s, ranges): 
     dt = make_datetime(s) 
     for begin,end in ranges: 
         if begin <= dt <= end: 
             return True 
     else: 
         return False 
ranges = [(make_datetime(b), make_datetime(e)) for (b,e) in [ 
     ('2008-12-18 23:59', '2009-01-12 00:00'), 
     ('2009-02-12 00:00', '2009-02-23 23:59'), 
     ('2009-04-02 00:00', '2009-04-20 23:59'),
     ('2009-05-21 00:00', '2009-06-01 23:59'),
     ('2009-07-21 00:00', '2009-08-12 23:59')
     ]] 

class MainPage(webapp.RequestHandler):
  def get(self):
    commons_sitting = 0
    lords_sitting = 0
    commons = get_feed("http://services.parliament.uk/calendar/commons.rss")
    lords = get_feed("http://services.parliament.uk/calendar/lords.rss")
    parliament = get_feed("http://twitter.com/statuses/user_timeline/6467332.atom")
    if commons.entries: commons_sitting = 1
    if lords.entries: lords_sitting = 1
    
    del parliament.entries[10:]

    for entry in parliament.entries:
        entry.title = entry.title[14:]
        
    # for entry in commons.entries:
    #     if entry.title == "Westminster Hall -": commons.entries.remove(entry)
    #     if entry.summary == "": commons.entries.remove(entry)
    template_values = {
      'today': datetime.today().strftime('%Y-%m-%d %H:%M'),
      'inRecessCommons': inRangeCommons(datetime.today().strftime('%Y-%m-%d %H:%M'), ranges),
      'inRecessLords': inRangeLords(datetime.today().strftime('%Y-%m-%d %H:%M'), ranges),
      'commons': commons,
      'lords': lords,
      'parliament': parliament,
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
