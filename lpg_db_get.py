# coding: utf-8

#this script fetches data form database
#and creates file for Andoid app
# {"timestamp":1234, "data": [array of{objects}] }

import xml.parsers.expat
import json, sys
import urllib2, urllib
from datetime import datetime

def save_js_to_file(js):
  
  d = json.dumps(js)

  f2 = open('output', 'w')
  f2.write(d)
  f2.close()


def get_timestamp():
  path = "http://lpg.site40.net/lpg_get.php"
  mydata = [('op','get_timestamp')]    #The first is the var name the second is the value

  mydata = urllib.urlencode(mydata)
  req = urllib2.Request(path, mydata)

  response = urllib2.urlopen(req).read()
  #print "------- start response -------- \n", response
  #print "------- end response ------- \n",
  pos = response.find("<")
  s = response
  if pos != -1:
    s = response[ : response.find("<")]
  #print s

  data = json.loads(s)
  if data['status'] == 0:
     print data['message']
  
  return data['timestamp']

def get_db_json():
  path = "http://lpg.site40.net/lpg_get.php"
  mydata = [('op','get_all')]    #The first is the var name the second is the value

  mydata = urllib.urlencode(mydata)
  req = urllib2.Request(path, mydata)

  response = urllib2.urlopen(req).read()
  pos = response.find("<")
  s = response
  if pos != -1:
    s = response[ : response.find("<")]

  data = json.loads(s)
  if data['status'] == 0:
     print data['message']
     return None;

  return data['data']

if __name__ == "__main__":
   t = get_timestamp()
   d = get_db_json()
   print "Got %d records"%(len(d))
   js = {}
   js['timestamp'] = t
   js['data'] = d
   save_js_to_file(js)
