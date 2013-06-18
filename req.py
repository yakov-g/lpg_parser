import urllib2, urllib

import json

mydata=[('one','1'),('two','2')]    #The first is the var name the second is the value
mydata=urllib.urlencode(mydata)
path='http://localhost/new.php'    #the url you want to POST to
p = "http://api.androidhive.info/android_connect/get_all_products.php"
p2 = "http://lpg.site40.net/lpg.php"
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
