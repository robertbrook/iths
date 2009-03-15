import os
import re
import urllib2
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson
import time 
from datetime import datetime 

def twitter_at_reply(tweet):
    pattern = re.compile(r"(\A|\W)@(?P<user>\w+)(\Z|\W)")
    repl = (r'\1<a href="http://twitter.com/\g<user>"'r' >@\g<user></a>\3')
    return pattern.sub(repl, tweet)
    
def v_to_i(text):
    return text.sub("\/","/")

def make_datetime(s, fmt='%Y-%m-%d %H:%M'): 
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
     ('2009-04-02 00:00', '2009-04-20 23:59'),
     ('2009-05-21 00:00', '2009-06-01 23:59'),
     ('2009-07-21 00:00', '2009-08-12 23:59')
     ]] 

class MainPage(webapp.RequestHandler):
  def get(self):
    aggregated = simplejson.load(urllib2.urlopen("http://pipes.yahoo.com/pipes/pipe.run?_id=2ebbec14ac85222b88f5a0481929dfd8&_render=json"))

    template_values = {
      'today': datetime.today().day,
      'inRecessCommons': inRangeCommons(datetime.today().strftime('%Y-%m-%d %H:%M'), ranges),
      'inRecessLords': inRangeLords(datetime.today().strftime('%Y-%m-%d %H:%M'), ranges),
      'aggregated': aggregated['value'],
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
