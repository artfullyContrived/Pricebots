#twitterbot
#jordan.dwo@gmail.com
import urllib2
import time
import json
from pprint import pprint

count = 0

#goes through iteration 9 times
while (count < 9) :
    #grabs conents from cryptowatch
    contents = \
        urllib2.urlopen("https://api.cryptowat.ch/markets/coinbase/ethusd/summary")\
        .read()
    data = json.loads(contents)

    #finds data
    last = data['result']['price']['last']
    high = data['result']['price']['high']
    low = data['result']['price']['low']
    percentage = data['result']['price']['change']['percentage']
    absolute_change = data['result']['price']['change']['absolute']
    volume = data['result']['volume']

    #puts into percentage format
    percentage = percentage * 100

    #turns data into string format
    last = "last: %5.2f" % last
    high = "high: %5.2f" % high
    low = "low: %5.2f" % low
    percentage = "percentage: %%%3.2f" % percentage
    absolute_change = "absolute_change: %3.2f" % absolute_change
    volume = "volume: %9.2f" % volume

    #prints data to console
    print last
    print high
    print low
    print percentage
    print absolute_change
    print

    #bot sleeps for 10 sec
    time.sleep(10)
    count = count + 1

print "All done!"
