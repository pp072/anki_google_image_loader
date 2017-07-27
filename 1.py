# -*- coding: utf-8  -*-
from __future__ import unicode_literals
__author__ = 'Pavel'
import os
import sys
import time
from urllib import FancyURLopener
from urllib import quote
import urlparse

import urllib2
import simplejson

# Define search term
searchTerm = 'ģimene'
searchTerm = quote(searchTerm.encode('utf8'))
# Start FancyURLopener with defined version
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()

# Set count to 0
count = 0

for i in range(0,2):
    # Notice that the start changes for each iteration in order to request a new set of images for each loop
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP')
    print url
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)

    # Get results using JSON
    results = simplejson.load(response)
    data = results['responseData']
    dataInfo = data['results']

    # Iterate for each result and get unescaped url
    for myUrl in dataInfo:
        count = count + 1
        print myUrl['unescapedUrl']

        path = urlparse.urlparse(myUrl['unescapedUrl']).path
        ext = os.path.splitext(path)[1]
        print ext
        if ext == "":
            ext = '.jpg'
        myopener.retrieve(myUrl['unescapedUrl'], str(count)+ext)

    # Sleep for one second to prevent IP blocking from Google
    time.sleep(1)