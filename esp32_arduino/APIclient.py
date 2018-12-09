import urllib
import json
import re
import sys

host = sys.argv[1]
port = sys.argv[2]
url = 'http://'+host+':'+port
print url

print "Select what command to request:"
print "\t(B) for begin"
print "\t(L) for move left"
print "\t(R) for move right"
print "\t(S) for stop"
option = raw_input(">> ")
# option = "B"
if len(option) == 1:
    option = option.upper()
    print "\t",option," was selected."
    p = re.compile(r'([BRLS]){1}')
    val = p.search(option)
    if val != None:

        try:
            contents = urllib.urlopen(url+'/'+option)
            data = contents.read()
            js = json.loads(data)
            print js
            # print json.dumps(js, indent=4)
        except:
            print "\tunable to request"
    else:
        print "\twrong command"