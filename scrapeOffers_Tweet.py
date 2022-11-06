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

def updateOffers(year,instId):
    # Read in old Offers
    dfOldOffers = pd.read_csv('data/offers_'+str(year)+'_'+str(instId)+'_old.csv')
    oldOffers = list(dfOldOffers.Key.unique()) # old Offers to list
    
    # Read new Offers
    dfNewOffers = getOffers(year,instId)
    newOffers = dfNewOffers[~dfNewOffers['Key'].isin(oldOffers)]
    
    if len(newOffers)>0:
        dfNewOffers.to_csv('data/offers_'+str(year)+'_'+str(instId)+'_old.csv',index=False)
        newOffers.reset_index(inplace=True,drop=True)
        for i in range(0,len(newOffers)):
            Name,Year,Stars,Rank,Pos,HT,WT,City,State,HS,Link = getRecruitmentInfo(newOffers.loc[i,'Recruitment'])
            tweetOffer(Name,Year,Stars,Rank,Pos,HT,WT,City,State,HS,Link)
    else:
        print('No New Offers')

def getOffers(year,instId):
    url = 'https://247sports.com/Season/'+str(year)+'-Football/RecruitInterests.json?Institution='+str(instId)+'&Offered=True&Items=500'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    return(dfFunc)

def getRecruitmentInfo(recruitmentId):
    url = 'https://247sports.com/recruitment/'+str(recruitmentId)+'/.json?'
    r = requests.get(url, headers={'User-Agent':'test'}) 
    jsonR = (json.loads(r.text))
    dfFunc = pd.json_normalize(jsonR) # create dataframe of recruits
    # print(dfFunc.loc[0])
    Name = dfFunc.loc[0,'Player.FullName']
    Year = dfFunc.loc[0,'Year'] 
    Stars = dfFunc.loc[0,'Player.CompositeStarRating']
    Rank = dfFunc.loc[0,'Player.NationalRank']
    Pos = dfFunc.loc[0,'Player.PrimaryPlayerPosition.Abbreviation']
    HT = dfFunc.loc[0,'Player.Height']
    WT = dfFunc.loc[0,'Player.Weight']
    City = dfFunc.loc[0,'Player.Hometown.City']
    State = dfFunc.loc[0,'Player.Hometown.State']
    HS = dfFunc.loc[0,'Player.PlayerHighSchool.Name']
    Link = dfFunc.loc[0,'Player.Url']
    return(Name,Year,Stars,Rank,Pos,HT,WT,City,State,HS,Link)

def tweetOffer(Name,Year,Stars,Rank,Pos,HT,WT,City,State,HS,Link):
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
        
    tweet = "🚨New #Gators Offer🚨\n\nRecruit Info\n🐊"+Name+" ("+str(Year)+")\n📈"+star_str+"(Rk #"+str(Rank)+")\n🏈"+Pos+"; "+str(HT)+"; "+str(WT)+"\n🏡"+City+', '+State+"\n🏫"+HS+"\n\n🔗"+Link
    # print(tweet)
    status = api.update_status(status=tweet)

if __name__ == "__main__":
    dfNewOffers = updateOffers(2023,24099)
    dfNewOffers = updateOffers(2024,24099)
    dfNewOffers = updateOffers(2024,24099)
    

