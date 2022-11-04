import os
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
    
print("TEST_SUCCESS")
    
def main():
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
 
    tweet = "🚨New #Gators 247 Crystal Ball🚨
         Recruit Info
        🐊Cormani McClain (2023)
        📈⭐️⭐️⭐️⭐️⭐️(Rk #2)
        🏈CB; 6-2; 165
        🏡Lakeland, FL
        🏫Lakeland
        Crystal Ball Info
        ✍️RCorySmith
        🎚️Confidence: 8
        https://247sports.com/Player/46109958"
    status = api.update_status(status=tweet)
 
if __name__ == "__main__":
    main()
