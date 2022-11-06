import os
import pandas as pd
import requests
import json
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

def updateCBs(year,instId):
    # Read in old Crystal Balls
    dfOldCBs = pd.read_csv('data/CB_'+str(year)+'_'+str(instId)+'_old.csv')
    dfOldCBs['UpdatedOn'] = pd.to_datetime(dfOldCBs['UpdatedOn'])
    lastUpdate = dfOldCBs.UpdatedOn.max() # get last update
    
    # Update crystal balls
    dfNewCBs = getCBs(year,instId)
    dfNewCBs['UpdatedOn'] = pd.to_datetime(dfNewCBs['UpdatedOn'])
    newUpdate = dfNewCBs.UpdatedOn.max()
    
    if newUpdate > lastUpdate:
        print('NEW CBs for '+str(year)+' - '+str(instId))
        dfNewCBs.to_csv('data/CB_'+str(year)+'_'+str(instId)+'_old.csv',index=False)
        dfNewCBs = dfNewCBs[dfNewCBs['UpdatedOn']>lastUpdate]
        dfNewCBs.reset_index(inplace=True,drop=True)
        for i in range(0,len(dfNewCBs)):
            playId = getPlayInstInfo(dfNewCBs.loc[i,'PlayerInstitution'])
            Name,CompositeStar,CompositeRank,Position,Height,Weight,Highschool,City,State = getPlayerInfo(playId)
            print(Name)
            user = getUserInfo(dfNewCBs.loc[i,'User'])
            state = dfStates[dfStates['Name']==State]['Abbreviation'].item()
            conf = dfNewCBs.loc[i,'Confidence']
            link = 'https://247sports.com/Player/'+str(playId)
            tweetIt(Name,year,CompositeStar,CompositeRank,Position,Height,
                    Weight,City+', '+state,Highschool,user,conf,link)
    else:
        print('NO NEW CBs for '+str(year)+' - '+str(instId))

def getCBs(year,instId):
    url = 'https://247sports.com/Season/'+str(year)+'-Football/CurrentExpertPredictions.json?OrderBy=UpdatedOn%3ADESC&Institution='+str(instId)
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    return(dfFunc)

def getPlayInstInfo(playInstId):
    url = 'https://247sports.com/PlayerInstitution/'+str(playInstId)+'/.json?'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    playId = dfFunc.loc[0,'Player']
    return(playId)

def getPlayerInfo(playId):
    url = 'https://247sports.com/Player/'+str(playId)+'/.json?'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    Name = dfFunc.loc[0,'FullName']
    CompositeStar = dfFunc.loc[0,'CompositeStarRating']
    CompositeRank = dfFunc.loc[0,'NationalRank']
    Position = dfFunc.loc[0,'PrimaryPlayerPosition.Abbreviation']
    Height = dfFunc.loc[0,'Height']
    Weight = dfFunc.loc[0,'Weight']
    Highschool = dfFunc.loc[0,'PlayerHighSchool.Name']
    City = dfFunc.loc[0,'Hometown.City']  
    State = dfFunc.loc[0,'Hometown.State']    
    return(Name,CompositeStar,CompositeRank,Position,Height,Weight,Highschool,City,State)

def getUserInfo(userId):
    url = 'https://247sports.com/User/'+str(userId)+'/.json?'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    user = dfFunc.loc[0,'Alias']
    return(user)

def tweetIt(name,year,stars,rank,pos,ht,wt,hometown,hs,user,conf,link):
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
    if stars == 5:
        star_str = '⭐️⭐️⭐️⭐️⭐️'
    elif stars ==4:
        star_str = '⭐️⭐️⭐️⭐️'
    elif stars == 3:
        star_str = '⭐️⭐️⭐️'   
    else:
        star_str = '⭐️⭐️'  
    tweet = "🚨New #Gators 247 Crystal Ball🚨\n\nRecruit Info\n🐊"+name+" ("+str(year)+")\n📈"+star_str+"(Rk #"+str(rank)+")\n🏈"+pos+"; "+str(ht)+"; "+str(wt)+"\n🏡"+hometown+"\n🏫"+hs+"\n\nCrystal Ball Info\n ✍️"+user+"\n🎚️Confidence: "+str(conf)+"\n\n🔗"+link
    # print(tweet)
    status = api.update_status(status=tweet)

if __name__ == "__main__":
    dfStates = pd.read_csv('data/states.csv')
    updateCBs(2023,24099)
    updateCBs(2024,24099)
    


