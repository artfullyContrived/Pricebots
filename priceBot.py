#twitterbot
#jordan.dwo@gmail.com
import urllib2
import time, datetime
import json
from pprint import pprint
import tweepy, time, sys

#argfile = str(sys.argv[1])

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'zQNh4UD3dTfdg6rchdE5WDwXE'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'vnNCSocmdKBkVvEmExQ6Bi3OlszIXoQxXNgtK2xeuv786cHITQ'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '840062077305724928-3aqfuyj6BuLhFslpkokrFXQjW3rU2dh'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'NNFzYUSwA6iWBaujUibUzRxgPcQEzzflUo5FaomYS8bE2'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


#for line in f:
#    api.update_status(line)
#    time.sleep(900)#Tweet every 15 minutes
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
    last = "Last: $%5.2f\n" % last
    high = "High: $%5.2f\n" % high
    low = "Low: $%5.2f\n" % low
    percentage = "Percentage: %3.2f%%\n" % percentage
    absolute_change = "Change: $%3.2f\n" % absolute_change
    volume = "Volume: $%9.2f\n" % volume

    tweet = "Ethereum price over last 24hrs:\n" + last + high + low + percentage \
        + absolute_change + volume + "$eth #Ethereum"

    #prints data to console
    print "Last tweet sent:"
    print datetime.datetime.utcnow()
    api.update_status(tweet)
    #bot sleeps for 10 sec
    time.sleep(60)
    count = count + 1

print "All done!"
