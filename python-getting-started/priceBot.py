#twitterbot
#jordan.dwo@gmail.com
import urllib2
import time, datetime, threading
import json
from pprint import pprint
import tweepy, time, sys

#argfile = str(sys.argv[1])

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'your key...'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'your secret...'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'your key...'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'your secret...'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def updateTweet ():
    threading.Timer(60,updateTweet).start()
    #grabs conents from cryptowatch
    contents = \
        urllib2.urlopen("https://api.cryptowat.ch/markets/coinbase/ethusd/summary")\
        .read()
    data = json.loads(contents)

    #finds data in contents
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

    #creates string for tweet
    tweet = "Ethereum price over last 24hrs:\n" + last + high + low + percentage \
        + absolute_change + volume + "$eth #Ethereum"

    #prints data to console
    print "Last tweet sent:" + str(datetime.datetime.utcnow())
    print "Just tweeted:\n" +str(tweet)
    print

    #tweets to witter
    api.update_status(tweet)

updateTweet ()
