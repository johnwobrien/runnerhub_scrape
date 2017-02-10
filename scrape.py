import requests
import json
from datetime import datetime, date
import calendar
import time
import unicodedata


def scrape():
    lastRun = 1475280962
    print 'Enter values (as integers) for earliest run to be looked at'
    year = input('year: ')
    month = input('month: ')
    day = input('day: ')
    #d = date(2017, 1, 1)
    d = date(year, month, day)
    timestamp1 = calendar.timegm(d.timetuple())
    #print timestamp1
    go = True
    gmDict = dict
    timestamp2 = 0
    total = 0
    # try:
    url_clean = 'https://www.reddit.com/r/runnerhub/new.json?sort=new'
    url = url_clean
    count = 0
    after = ""
    gmDict = {}
    while go:
        page = requests.get(url)
        js = json.loads(page.content)
        if 'data' in js:
            data = js['data']['children']
            for a in data:
                flair = unicodedata.normalize('NFKD', a['data']['link_flair_text']).encode('ascii','ignore')
                if 'Positions Filled' in flair or 'Help Wanted' in flair:
                    if int(a['data']['created_utc']) < timestamp1:
                        #print a['data']['created_utc']
                        go = False
                        break;
                    total = total + 1
                    if not a['data']['author'].lower() in gmDict:
                        gmDict[a['data']['author'].lower()] = 1
                    else:
                        gmDict[a['data']['author'].lower()] = gmDict[a['data']['author'].lower()] + 1

                    timestamp2 = a['data']['created_utc']
            count = count + 25
            try:
                after = js['data']['after']
                url = url_clean + "?count=" + str(count) + "&after=" + after
                #print url
            except KeyError:
                print "KeyError1 on url " + url
                go = False
            except TypeError:
                print "-----------------------------------------"
                print 'Data that far back is not available'
                go = False
    print "-----------------------------------------"
    for key in sorted(gmDict.iterkeys()):
        print "%s: %i" % (key, gmDict[key])
    print "-----------------------------------------"

    print "total Runs: %i" % (total)
    print "total GMs : %d" % len (gmDict)
    print "Earliest run looked at: %s" % str(datetime.fromtimestamp(timestamp2))
    
scrape()
