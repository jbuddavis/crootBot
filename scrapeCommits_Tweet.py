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

def updateCommits(year,instId):
    # Read in old Commits
    dfOldCommits = pd.read_csv('data/commits_'+str(year)+'_'+str(instId)+'_old.csv')
    oldCommits = list(dfOldCommits.Key.unique()) # old Commits to list
    
    # Read new Commits
    dfNewCommits = getCommits(year,instId)
    newCommits = dfNewCommits[~dfNewCommits['Key'].isin(oldCommits)]

    
    if len(newCommits)>0:
        dfNewCommits.to_csv('data/commits_'+str(year)+'_'+str(instId)+'_old.csv',index=False)
        newCommits.reset_index(inplace=True,drop=True)
        for i in range(0,len(newCommits)):
            try:
                Name,Year,Stars,Rank,PosKey,Pos,HT,WT,City,State,HS,Link = getRecruitmentInfo(int(newCommits.loc[i,'Player.PrimaryRecruitment']))
                tweetCommitment(Name,Year,Stars,Rank,Pos,HT,WT,City,State,HS,Link)
            except:
                tweetCommitment(newCommits.loc[i,'DefaultName'],
                                year,
                                newCommits.loc[i,'Player.CompositeStarRating'],
                                newCommits.loc[i,'Player.NationalRank'],
                                newCommits.loc[i,'Player.PrimaryPlayerPosition.Abbreviation'],
                                newCommits.loc[i,'Player.Height'],
                                newCommits.loc[i,'Player.Weight'],
                                newCommits.loc[i,'Player.Hometown.City'],
                                newCommits.loc[i,'Player.Hometown.State'],
                                newCommits.loc[i,'Player.PlayerHighSchool.Name'],
                                newCommits.loc[i,'Player.Url'])
    else:
        print('no new Commits')
    return(dfNewCommits)

def getCommits(year,instId):
    url = 'https://247sports.com/Season/'+str(year)+'-Football/Recruits.json?CommittedInstitution='+str(instId)+'&items=500'
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

def tweetCommitment(Name,Year,Stars,Rank,Pos,HT,WT,City,State,HS,Link):
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
        
    tweet = "🚨New #Gators Commitment🚨\n\nRecruit Info\n🐊"+Name+" ("+str(Year)+")\n📈"+star_str+"(Rk #"+str(Rank)+")\n🏈"+Pos+"; "+str(HT)+"; "+str(WT)+"\n🏡"+City+', '+State+"\n🏫"+HS+"\n\n🔗"+Link
    # print(tweet)
    status = api.update_status(status=tweet)

if __name__ == "__main__":
    dfStates = pd.read_csv('data/states.csv')
    updateCommits(2023,24099)
    updateCommits(2024,24099)


