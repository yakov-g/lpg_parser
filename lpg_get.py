# coding: utf-8

import xml.parsers.expat
import json, sys
import urllib2, urllib
from datetime import datetime

ST_NONE = "ST_NONE"
ST_PLCMRK = "ST_PLCMRK"
ST_DESC = "ST_DESC"
ST_NAME = "ST_NAME"
ST_COORD = "ST_COORD"

class XMLparser(object):
# 3 handler functions
  def __init__(self):
     self.state = ST_NONE
     self.lst = []

  def start_element(self, name, attrs):
     #print 'Start element:', name, attrs
     self.cur_str = ""
     if name == 'Placemark':
        if self.state == ST_NONE:
          self.state = ST_PLCMRK
          self.cur = {}
        else:
          print "Error: found open %s, but state is non NONE"%(name)
          print name
     elif name == 'name':
        if self.state == ST_PLCMRK:
           self.state = ST_NAME
        else:
          print "Error: found open %s, but state is non %s; but %s"%(name, ST_PLCMRK, self.state)
          print name
     elif name == 'coordinates':
        if self.state == ST_PLCMRK:
           self.state = ST_COORD
        else:
          print "Error: found open %s, but state is non %s"%(name, ST_PLCMRK)
          print name
     elif name == 'description':
        if self.state == ST_PLCMRK:
           self.state = ST_DESC
        else:
          print "Error: found open %s, but state is non %s"%(name, ST_PLCMRK)
          print name
        

  def end_element(self, name):
     #print 'End element:', name
     if name == 'Placemark':
        if self.state == ST_PLCMRK:
          self.state = ST_NONE
          #print self.cur
          #print self.cur['name'].encode("utf-8")
          self.lst.append(self.cur)
          return
        else:
          print "Error: found close %s, but state is non %s; state is %s"%(name, ST_PLCMRK, self.state)
          print name
          return
     elif name == 'name':
        if self.state == ST_NAME:
           self.state = ST_PLCMRK
        else:
          print "Error: found close %s, but state is non %s"%(name, ST_NAME)
          print name
          return
     elif name == 'coordinates':
        if self.state == ST_COORD:
           self.state = ST_PLCMRK
        else:
          print "Error: found close %s, but state is non %s"%(name, ST_COORD)
          print name
          return
     elif name == 'description':
        if self.state == ST_DESC:
           self.state = ST_PLCMRK
        else:
          print "Error: found close %s, but state is non %s"%(name, ST_DESC)
          print name
          return
     else:
        return
     self.cur[name] = self.cur_str

  def char_data(self, data):
     f2 = open('/home/yakov/Downloads/output', 'a')
     if self.state == ST_NAME:
       #print 'Name:', data
       self.cur_str += data
       #f2.write(unicode(st))
     elif self.state == ST_COORD:
       #print 'Coord:', data
       self.cur_str += data
     elif self.state == ST_DESC:
       #print 'Desc:', data
       self.cur_str += data

     #print 'Character data:', data

  def parse(self, fname):  
     #f = open(fname, 'r')
     #allfile = f.read()
     #pirint allfile
     p = xml.parsers.expat.ParserCreate()

     p.StartElementHandler = self.start_element
     p.EndElementHandler = self.end_element
     p.CharacterDataHandler = self.char_data

     p.ParseFile(open(fname, 'r'))
     #p.Parse("""<?xml version="1.0"?>
     #      <parent id="top"><child1 name="paul">Text goes here</child1>
     #      <child2 name="fred">More text</child2>
     #      </parent>""", 1)

def main():
  
  print sys.argv
  fname = sys.argv[1]
  xp = XMLparser()
  xp.parse(fname)

  for l in xp.lst:
    coord_lst = l['coordinates'].split(',')
    #latitude and longitude are mixed in google's kml file
    #so need to reorder it
    l["lat"] = float(coord_lst[1])
    l["lng"] = float(coord_lst[0])
    del l['coordinates']

    desc = l['description']
    desc_lst = desc.split('<br>')
    time_str = desc_lst[2]
    pos = time_str.find("<")
    time_str = time_str[:pos]
    l["time"] = u"\u200e" + time_str
    del l['description']
    l["name"] = u"\u200e" + l["name"]
  
  #print xp.lst
  d = json.dumps(xp.lst)


  f2 = open('output', 'w')
  f2.write(d)
  print "Stations qty: ", len(xp.lst)
  print datetime.utcnow()

  mydata=[('op','1'),('time','987654321'), ('json', d)]    #The first is the var name the second is the value
  mydata=urllib.urlencode(mydata)
  p2 = "http://lpg.site40.net/lpg_db_reload.php"
  req=urllib2.Request(p2, mydata)
  #req.add_header("Content-type", "application/x-www-form-urlencoded")
  page=urllib2.urlopen(req).read()
  print page

def get_data():
  mydata=[('op','2'), ('id', 1409)]    #The first is the var name the second is the value
  mydata=urllib.urlencode(mydata)
  p2 = "http://lpg.site40.net/lpg_db_reload.php"
  req=urllib2.Request(p2, mydata)
  #req.add_header("Content-type", "application/x-www-form-urlencoded")
  page=urllib2.urlopen(req).read()
  print page
  s = page[ : page.find("<")]
  print s

  data = json.loads(s)
  print data['id']
  print data['name']
  print data['time']

if __name__ == "__main__":
   #main()
   get_data()
