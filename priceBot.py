#twitterbot
#jordan.dwo@gmail.com
import requests
import time, datetime, threading, tweepy, sys
import json
import plotly.offline as offline
import plotly.graph_objs as go
import os
from subprocess import Popen

#enter the corresponding information from your Twitter application:
#keep the quotes, replace this with your consumer key
CONSUMER_KEY = 'secret...'
#keep the quotes, replace this with your consumer secret key
CONSUMER_SECRET = 'secret...'
#keep the quotes, replace this with your access token
ACCESS_KEY = 'secret...'
#keep the quotes, replace this with your access token secret
ACCESS_SECRET = 'secret...'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60
EPSILON = MINUTE * 2

#finds users operating system
name = os.name
#creates download_folder's path based of os
if name == 'nt':
    print 'Operating System is Windows.'
    download_folder = os.path.expanduser('~')+'\Downloads\\'
    print 'Downloads folder is '+ download_folder
    browser = 'chrome.exe'
    print browser
else:
    print 'Operating System is Linux'
    download_folder = os.path.expanduser('~')+'/Downloads/'
    print 'Downloads folder is '+download_folder
    browser = 'chromium-browser'
    print browser

def plotTweet():
    # for getting interval of OHLC data from cyrptowatch
    now =  int(time.time())
    date = int(time.time() - WEEK)

    # prints out to console
    print "Last week:  %9.0f" % date
    print datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    print "\nNow: %9.0f" % now
    print datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    print

    # parameters for grabbing specific content form cyrptowatch
    params = {'after': date, 'before': now, 'periods': HOUR}

    # grabs OHCL contents from cryptowatch
    r = requests.get("https://api.cryptowat.ch/markets/coinbase/ethusd/ohlc",
                    params=params)
    data = r.json()

    # puts json data into list with each element being a candle
    data = data['result'][str(HOUR)]

    # initializing lists for OHCL data
    dates = list()
    open_data = list()
    high_data = list()
    low_data = list()
    close_data = list()
    volume_data = list()

    # reading data form each candle into OHCL lists
    for candle in data:
        #puts day for each candle into datetime for plotting
        day = candle[0]
        day = datetime.datetime.fromtimestamp(day).strftime('%Y-%m-%d %H:%M:%S')
        dates.append(day)

        open_data.append(candle[1])
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])
        volume_data.append(candle[5])


    # traces the data for plot
    trace = go.Candlestick(x=dates,
                           open=open_data,
                           high=high_data,
                           low=low_data,
                           close=close_data,
                           increasing=dict(name='<i>Bullish Hour</i>',
                                line=dict(color= '#19cf86')
                                ),
                           decreasing=dict(name='<i>Bearesh Hour</i>',
                               line=dict(color= '#cf1962')
                               )
                           )
    data = [trace]

    # attributes for plot
    cwd = os.getcwd()
    layout = \
        go.Layout(
        title='Ethereum Price',
        titlefont=dict(
            family='Courier New, monospace',
            size=34,
            color='#7f7f7f'
            )
        ,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            ),
            title='Past Seven Days (UTC Time)<br>',
            showgrid= True,
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='USD',
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            ),
            side='right'
        ),
        paper_bgcolor= '#f5e6d1',
        plot_bgcolor= '#f5e6d1',
        legend = dict(
            x = -.1,
            y = -.25,
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            ),
        ),
        images=[dict(
            source= 'https://raw.githubusercontent.com/JordanDworaczyk/EthPriceBot/Issue-%2315/watermark.png',
            xref='paper', yref='paper',
            x=.95, y=-.4,
            sizex=0.2, sizey=0.2,
            opacity=0.1,
            xanchor='left', yanchor='bottom'
        )]
    )
    print cwd
    # combines data and layout into figure
    fig = go.Figure(data=data, layout=layout)

    #plots figure, saves as html, saves pic of tweet into downloads folder
    offline.plot(fig, image='png',image_filename='plot',auto_open=True)



#forces tweet to initiate on the hour
now = time.time()
round(now)
while now % HOUR > EPSILON:
    print 'Waiting to tweet.'
    now = time.time()
    round(now)
    time.sleep(MINUTE / 2)

def updateTweet ():
    #after tweet has been initiated it will start every hour again
    print 'Sleeping...'
    threading.Timer(HOUR, updateTweet).start()
    print 'updating tweet.'

    #grabs contents from cryptowatch
    r=requests.get("https://api.cryptowat.ch/markets/coinbase/ethusd/summary")
    data = r.json()

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
    percentage = "Change: %3.2f%%" % percentage
    absolute_change = " | $%3.2f\n" % absolute_change
    volume = "Volume: $%9.2f\n" % volume

    #creates string for tweet
    tweet = "#Eth 24hr Summary:\n" + last + high + low + percentage \
        + absolute_change + volume + "$eth #Ethereum #coinbase"

    now = datetime.datetime.now()

    #calls plot function
    plotTweet()
    #sleeps to allow time for plot.png to be downloaded into folder
    time.sleep(15)
    #tweets to twitter with picture and tweet status
    api.update_with_media(download_folder+'plot.png', status=tweet)
    # removes picture from file after tweeted
    os.remove(download_folder+'plot.png')

    #prints data to console
    print "Last tweet sent:" + now.strftime('%Y/%m/%d/ %I:%M:%p')
    print "Just tweeted:\n" +str(tweet)
    print

    time.sleep(HOUR / 2)
    #clears chrome window to avoid openning too many tabs and crashing system
    if browser == 'chrome.exe':
        Popen(['taskkill ', '/F',  '/IM', browser], shell=False)
    elif browser == 'chromium-browser':
        Popen(['taskkill ', '/F',  '/IM', browser], shell=False)
    else:
        print 'Cannot find browser to kill.'

#calls update again to run until program is exited out
updateTweet ()
