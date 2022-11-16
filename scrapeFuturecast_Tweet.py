import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import tweepy

try:
    twitter_ck = os.environ["TWITTER_CK"]
    twitter_cs = os.environ["TWITTER_CS"]
    twitter_t = os.environ["TWITTER_T"]
    twitter_ts = os.environ["TWITTER_TS"]
except KeyError:
    twitter_ck = "key not available!"
    twitter_cs = "key not available!"
    twitter_t = "key not available!"
    twitter_ts = "key not available!"

def updateFuturecast():
    # Read in old Futurecast
    dfFuturecast_old = pd.read_csv('data/futurecasts_old.csv')
    oldFuturecast = list(dfFuturecast_old.text.unique()) # old Futurecast to list
    
    # Read new Futurecast
    dfFuturecast_new = getFuturecast()
    newFuturecast = dfFuturecast_new[~dfFuturecast_new['text'].isin(oldFuturecast)]
  
    if len(newFuturecast)>0:
        dfFuturecast_new.to_csv('data/futurecasts_old.csv',index=False)
        newFuturecast.reset_index(inplace=True,drop=True)
        for i in range(0,len(newFuturecast)):
            try:
                tweetFuturecast(newFuturecast.loc[i,'text'],
                                newFuturecast.loc[i,'link'])
            except:
                print('error reading new futurecast')
    else:
        print('no new Futurecast')

def getFuturecast():
    url3 = 'https://florida.rivals.com/futurecast' # create url for to scrape HS information
    r = requests.get(url3, headers={'User-Agent':'test'}) # get from 247
    soup = BeautifulSoup(r.content, "html.parser") # scrape page with BS
    
    # Get forecasts
    forecast = soup.find_all("div", class_="ForecastActivity_forecastText__tdsTe")    
     # create empty lists
    text = []
    link = []
    # search for forecast text and append to list
    for th in forecast:
        text.append(th.text)
    # search for forecast links and append to list
    for a in forecast:
        for b in a.find_all('a', href=True, text=True):
            link.append(b['href'])
    link = [x for x in link if "prospects" in x] # filter out referers
    # create dataframe
    dfFunc = pd.DataFrame({'text': text,'link': link,})
    return(dfFunc)


def tweetFuturecast(Text,Link):
    twitter_auth_keys = {
        "consumer_key"        : twitter_ck,
        "consumer_secret"     : twitter_cs,
        "access_token"        : twitter_t,
        "access_token_secret" : twitter_ts
    }
 
    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
    Text = Text.replace(')   to',') to')
    tweet = "🚨New #Gators Rivals Futurecast🚨\n\n"+Text+"\n\n🔗"+Link
    # print(tweet)
    status = api.update_status(status=tweet)

if __name__ == "__main__":
    updateFuturecast()


