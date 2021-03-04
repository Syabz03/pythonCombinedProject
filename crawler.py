import tweepy
import praw
from mydata import *

class crawler:
    data =''
    url=''

    def search(self):
        pass

    def format(self, block):
        pass

    
class redditCrawler(crawler):
    reddit=''

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id='PESO3cS0KquaWQ', 
            client_secret='ALSLenkZwZ5WCZ-32MaziUw-O7tmeA', 
            user_agent='VanillaCast'
        )

    def search(self,input):
        input = "GPU"
        for submission in self.reddit.subreddit("all").search(input,'hot',limit=10):
            block = Mydata(input)
            block.addComment(submission.title)
            iCount = submission.upvote_ratio
            iCount = submission.score/(iCount-(1-iCount))
            iCount *= 100
            block.addLikeCount(int(iCount))
        
        print(block.interactionCount)
        for c in block.topComments:
            print(c)
        
        return block
            # print("Title: ",submission.title)
            # print("Author: ",submission.author)
            # print("link: ",submission.permalink)
            # print("updoot: ",submission.score)
            # print("upvote ratio: ",submission.upvote_ratio)
            # print("comment count:",submission.num_comments)
            # commentTree = submission.comments
            # print("comment 1",commentTree[0].body)

    
    def format(self, block):
        #return data obj
        pass

class twitterCrawler(crawler):

    queryLimit = 5

    def __init__(self):
        consumer_key = "VpNVndPOykZXjQgfTg2RD21xz"
        consumer_secret = "1LyM7m5lTmNWwzUUSJF2kN04B5bZvRStY663PjNEnQRCS6b2QW"
        access_token = "1358367734417903620-liyj12fLuUrQGM09nsqiVqiAsFKuRc"
        access_token_secret = "r5O5AQYHDZrddrPki5FKDZUritllO3VRSoCIlHJv84UEA"

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Creating the authentication object
        self.auth.set_access_token(access_token, access_token_secret) # Setting your access token and secret

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True) # Creating the API object while passing in auth information

    def search(self,input):
        
        results = self.api.search(q=input, lang="en", rpp=self.queryLimit) #initiate API call

        # Temp tweet print function
        print("\n========================================Twitter Result===========================================\n")
        index = 1
        for tweet in results:
            print(str(index) + ") " + tweet.user.screen_name + "> " + tweet.text)
            index += 1

        return results

    def format(self, block):
        return super().format(block)