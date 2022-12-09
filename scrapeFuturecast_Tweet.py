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
    oldFuturecast = list(dfFuturecast_old.check.unique()) # old Futurecast to list
    
    # Read new Futurecast
    dfFuturecast_new = getFuturecast()
    newFuturecast = dfFuturecast_new[~dfFuturecast_new['check'].isin(oldFuturecast)]
  
    if len(newFuturecast)>0:
        dfFuturecast_new.to_csv('data/futurecasts_old.csv',index=False)
        newFuturecast.reset_index(inplace=True,drop=True)
        for i in range(0,len(newFuturecast)):
            try:
                tweetFuturecast(newFuturecast.loc[i])
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
    
    # Get Forecast Text
    dfFunc = pd.DataFrame()
    for i in range(0,len(forecast)):
        j = 0
        for th in forecast[i]:
            j = j+1    
            # print(th.text)
            dfFunc.loc[i,j]=th.text
    dfFunc = dfFunc.drop(columns=[4,5,7,8,9])
    dfFunc.rename(columns={1: "predictor", 2: "forecast",
                       3: "recruit", 6:'properties',
                       10: "destination"}, inplace=True)
    dfFunc['check'] = dfFunc['predictor']+' '+dfFunc['recruit']+' '+dfFunc['destination']
        
    # search for forecast links and append to list
    link = []
    for a in forecast:
        for b in a.find_all('a', href=True, text=True):
            link.append(b['href'])
    link = [x for x in link if "prospects" in x] # filter out referers
    dfFunc['link'] = link
    return(dfFunc)


def tweetFuturecast(dfFunc):
    Text = dfFunc['predictor']+' '+dfFunc['forecast']+' '+dfFunc['recruit']+' '+dfFunc['properties']+' '+dfFunc['destination']
    Link = dfFunc['link']
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



