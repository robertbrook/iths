import os
import feedparser
import re
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import time 
from datetime import datetime 

def twitter_at_reply(tweet):
    pattern = re.compile(r"(\A|\W)@(?P<user>\w+)(\Z|\W)")
    repl = (r'\1<a href="http://twitter.com/\g<user>"'
    r' >@\g<user></a>\3')
    return pattern.sub(repl, tweet)

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
    tweetminster = get_feed("http://feeds2.feedburner.com/TweetminsterLivestreamMpsWhoTweet")
    news = get_feed("http://news.parliament.uk/feed/atom/")	

    if commons.entries: commons_sitting = 1
    if lords.entries: lords_sitting = 1
    
    #del parliament.entries[10:]

    for entry in parliament.entries:
        entry.title = entry.title[14:]
        entry.title = twitter_at_reply(entry.title)

    for entry in tweetminster.entries:
        #words = re.split('\W+', entry.title,1)
        entry.title = '@' + entry.title
        #entry.title = 'http://twitter.com/' + words[0] + ' ' + words[1]
        entry.title = twitter_at_reply(entry.title)

    template_values = {
      'today': datetime.today().day,
      'inRecessCommons': inRangeCommons(datetime.today().strftime('%Y-%m-%d %H:%M'), ranges),
      'inRecessLords': inRangeLords(datetime.today().strftime('%Y-%m-%d %H:%M'), ranges),
      'commons': commons,
      'lords': lords,
      'parliament': parliament,
      'news': news,
      'commons_sitting': commons_sitting,
      'lords_sitting': lords_sitting,
      'tweetminster': tweetminster,
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
