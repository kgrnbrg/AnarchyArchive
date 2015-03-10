import pytumblr
import sys
import os
import time
import urllib
from urllib import FancyURLopener
import urllib2
import simplejson
import newspaper
import requests
import re
from bs4 import BeautifulSoup

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

# Start FancyURLopener with defined version 
class MyOpener(FancyURLopener): 
  version = 'Chrome'
myopener = MyOpener()

#searchTerm = newspaper.hot()[0]
page = urllib2.urlopen('http://www.google.com/trends/').read()
soup = BeautifulSoup(page)
mydivs = soup.findAll("div", { "class" : "landing-page-hottrends-image-and-info-row-container" })
myspans = [div.span for div in mydivs]
search_term_list = [span.getText() for span in myspans]
searches_spans = soup.findAll("span", { "class" : "hottrends-single-trend-info-line-number" })
search_num_list = [span.getText().replace(",","")[:-1] for span in searches_spans]
search_num_list = map(int, search_num_list)
## THIS IS THE NUMBER YOU WANT
top_hit_num = max(search_num_list)
search_index = search_num_list.index(top_hit_num)
searchTerm = search_term_list[search_index]


# def get_caption(titles):
#   caption = ""
#   for title in titles:
#       caption += title + '\n'
#   return caption

# ouath_data = open("oauth.txt")

# # get all keys
# keys = ouath_data.read()
# keys_decoded = keys.decode("utf-8-sig")
# keys = keys_decoded.encode("utf-8")
# keys = keys.rstrip().split('\n')
def search_party ():
# Get top Google Trend
  

  # Replace spaces ' ' in search term for '%20' in order to comply with request
  searchTermSyntax = searchTerm.replace(' ','%20')


  # Notice that the start changes for each iteration in order to request a new set of images for each loop
  url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTermSyntax+'&start='+str(0)+'&userip=MyIP')
  #urllib.urlretrieve(url, "image"  str(i)  ".jpg")
  request = urllib2.Request(url, None, {'Referer': 'testing'})
  response = urllib2.urlopen(request)

  # Get results using JSON
  results = simplejson.load(response)
  data = results['responseData']
  dataInfo = data['results']

  # Get unescaped url for first result
  myopener.retrieve(dataInfo[0]['unescapedUrl'],searchTerm+'.jpg')


def get_titles():

  # Replace spaces ' ' in search term with '+' for bing requests
  bingSearchTermSyntax = searchTerm.replace(' ','+')

  # get top news articles from Bing
  page = urllib2.urlopen('http://www.bing.com/news/search?q='+bingSearchTermSyntax+'&FORM=HDRSC6').read()
  soup = BeautifulSoup(page)

  mydivs = soup.findAll('div', {'class':'newstitle'})
  links = [div.findAll('a') for div in mydivs]


  titles = [link[0].contents for link in links]


  new_titles = []


# each title comes in as a list (ie - [<strong>Daylight</strong>, u' ', <strong>Saving</strong>, u' ', <strong>Time</strong>, u' Starts Sunday at 2 a.m.'])
# this loop concatenates the list as a string and removes html tags
  for title in titles:
    new_title = ''.join(str(v.encode('utf-8')) for v in title)
    new_title = remove_tags(new_title)
    new_titles.append(new_title)
  return new_titles



# # post photo to tumblr
# client.create_photo("anarchyarchive", caption=get_caption(new_titles), state="published" , data=searchTerm.encode('utf-8') + ".jpg")