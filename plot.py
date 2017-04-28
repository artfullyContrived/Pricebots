import plotly.offline as offline
import plotly.graph_objs as go
import plotly
import urllib

offline.plot({'data': [{'y': [4, 2, 3, 4]}],
               'layout': {'title': 'Test Plot',
                          'font': dict(size=16)}})

#help(plotly.offline.plot)
resource = urllib.urlopen("file:///C:/Users/jdwor/git/EthPriceBot/temp-plot.jpeg")
output = open("file01.jpg","wb")
output.write(resource.read())
output.close()
