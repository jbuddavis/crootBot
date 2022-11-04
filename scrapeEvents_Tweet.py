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

def updateEvents():
    # Read in old Events
    dfPositions = pd.read_csv('positions.csv')
    dfOldEvents = pd.read_csv('events_old.csv')
    oldEvents = list(dfOldEvents.Key.unique()) # old events to list
    
    # Read new events
    dfNewEvents = getEvents()
    dfNewEvents = dfNewEvents[(dfNewEvents['Type']=='OfficialVisit')|(dfNewEvents['Type']=='HardCommit')]
    dfNewEvents['Date'] = pd.to_datetime(dfNewEvents['Date'])
    newEvents = dfNewEvents[~dfNewEvents['Key'].isin(oldEvents)]
    
    if len(newEvents)>0:
        dfNewEvents.to_csv('events_old.csv')
        newEvents.reset_index(inplace=True,drop=True)
        for i in range(0,len(newEvents)):
            Name,Year,Stars,Rank,PosKey,Pos,HT,WT,City,State,HS,Link = getRecruitmentInfo(newEvents.loc[i,'Recruitment'])
            Sport = dfPositions[dfPositions['Key']==PosKey]['Sport'].item()
            Date = newEvents.loc[i,'Date'].strftime('%m/%d/%y')
            if newEvents.loc[i,'Type'] == 'OfficialVisit':
                tweetOV(Name,Year,Stars,Rank,Sport,Pos,HT,WT,City,State,HS,Date,Link)
            else:
                tweetCommitment(Name,Year,Stars,Rank,Sport,Pos,HT,WT,City,State,HS,Link)
    else:
        print('no new events')

def getEvents():
    url = 'https://247sports.com/college/florida/Institution/24099/RecruitInterestEvents.json?OrderBy=Date%3ADESC'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    return(dfFunc)

def getRecruitmentInfo(recruitmentId):
    url = 'https://247sports.com/recruitment/'+str(recruitmentId)+'/.json?'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    Name = dfFunc.loc[0,'Player.FullName']
    Year = dfFunc.loc[0,'Year'] 
    Stars = dfFunc.loc[0,'Player.CompositeStarRating']
    Rank = dfFunc.loc[0,'Player.NationalRank']
    PosKey = dfFunc.loc[0,'Position']
    Pos = dfFunc.loc[0,'Player.PrimaryPlayerPosition.Abbreviation']
    HT = dfFunc.loc[0,'Player.Height']
    WT = dfFunc.loc[0,'Player.Weight']
    City = dfFunc.loc[0,'Player.Hometown.City']
    State = dfFunc.loc[0,'Player.Hometown.State']
    HS = dfFunc.loc[0,'Player.PlayerHighSchool.Name']
    Link = dfFunc.loc[0,'Player.Url']
    return(Name,Year,Stars,Rank,PosKey,Pos,HT,WT,City,State,HS,Link)

def getUserInfo(userId):
    url = 'https://247sports.com/User/'+str(userId)+'/.json?'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    user = dfFunc.loc[0,'Alias']
    return(user)

def tweetOV(Name,Year,Stars,Rank,Sport,Pos,HT,WT,City,State,HS,Date,Link):
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
    if Stars == 5:
        star_str = '⭐️⭐️⭐️⭐️⭐️'
    elif Stars ==4:
        star_str = '⭐️⭐️⭐️⭐️'
    elif Stars == 3:
        star_str = '⭐️⭐️⭐️'   
    else:
        star_str = '⭐️⭐️' 
        
    if Sport == 1:
        sport_str = '🏈'
    elif Sport ==2:
        sport_str = '🏀'
    elif Sport == 3:
        sport_str = '⚾️' 
    tweet = "🚨New #Gators Official Visit🚨\n\nRecruit Info\n🐊"+Name+" ("+str(Year)+")\n📈"+star_str+"(Rk #"+str(Rank)+")\n"+sport_str+Pos+"; "+str(HT)+"; "+str(WT)+"\n🏡"+City+', '+State+"\n🏫"+HS+"\n🗓️"+Date+"\n\n🔗"+Link
    # print(tweet)
    status = api.update_status(status=tweet)

def tweetCommitment(Name,Year,Stars,Rank,Sport,Pos,HT,WT,City,State,HS,Link):
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
    if Stars == 5:
        star_str = '⭐️⭐️⭐️⭐️⭐️'
    elif Stars ==4:
        star_str = '⭐️⭐️⭐️⭐️'
    elif Stars == 3:
        star_str = '⭐️⭐️⭐️'   
    else:
        star_str = '⭐️⭐️' 
        
    if Sport == 1:
        sport_str = '🏈'
    elif Sport ==2:
        sport_str = '🏀'
    elif Sport == 3:
        sport_str = '⚾️' 
    tweet = "🚨New #Gators Commitment🚨\n\nRecruit Info\n🐊"+Name+" ("+str(Year)+")\n📈"+star_str+"(Rk #"+str(Rank)+")\n"+sport_str+Pos+"; "+str(HT)+"; "+str(WT)+"\n🏡"+City+', '+State+"\n🏫"+HS+"\n\n🔗"+Link
    # print(tweet)
    status = api.update_status(status=tweet)

if __name__ == "__main__":
    dfStates = pd.read_csv('states.csv')
    updateEvents()
    

