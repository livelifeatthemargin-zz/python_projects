import json
import urllib
from pprint import pprint
from itertools import combinations, permutations
import operator
import requests
import re

listofcurrencies = ["USD","EUR","AUD","JPY","GBP","CAD","CHF","NZD"] #"INR","CNY","THB"
posslist2 = []
posslist = []
currcombo = []
#texturl = 'http://rate-exchange.appspot.com/currency?from=GBP&to=EUR'
currdic = {}
value = []
finallist = []

def getallposs(list):
    posslist = [':'.join(p) for x in range(len(list)) for c in combinations(list, x+1) for p in permutations(c)]
    for poss in posslist:
        text = poss.split(":")
        if len(text)>2:
            newtext = str(poss + ":" + text[0])
            posslist2.append(newtext)
        elif len(text)>1:
            newtext2 = str(poss + ":")
            currcombo.append(newtext2)
            #print currcombo

def getcurrex(list):
    getallposs(list)
    for curr in currcombo:
        thetext = curr.split(":")
        first_id = thetext[0]
        second_id = thetext[1]
        texturl = 'http://rate-exchange.appspot.com/currency?from={}&to={}'.format(first_id, second_id)
        jsonurl = requests.get(texturl)
        data = jsonurl.json()
        #print data['rate']

        currdic[curr] = data['rate']
    
    print currdic

def arbitrage(thelist):
    getcurrex(thelist)
    for poss in posslist2:
        gettext = poss.split(":")
        #print gettext
        thevalue = 1
        for x in range(0,len(gettext)-1):
            newcombo = str(gettext[x:x+2])
            finalcombo = str(newcombo[2:5] + ":" + newcombo[9:12] + ":")
            #print finalcombo
            #print currdic[finalcombo]
            thevalue = thevalue * currdic[finalcombo]
        value.append(thevalue)
        finallist.append(str(poss + " " + str(thevalue)))
        #print finallist

def getbest(thelist):
    arbitrage(thelist)
    values = {}
    for value in finallist:
        try:
            [path, increase] = value.strip().split()
            values[path] = increase
        except:
            pass
    sorted_values = sorted(values.iteritems(), key = operator.itemgetter(1))
    highest_value = sorted_values[-1]
    percent_incr = float((float(highest_value[1])-1)*100)
    #print sorted_values
    print (str(highest_value[0]) + " " + str(percent_incr) + " Percent Increase")

getbest(listofcurrencies)    
    
    #getallposs(listofcurrencies)
