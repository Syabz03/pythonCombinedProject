import tweepy
import praw
import prawcore
from mydata import *

class crawler:
    data =''
    topic = ''

    def search(self):
        pass

    def format(self, block):
        pass

    
class redditCrawler(crawler):
    reddit=''

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id='zo7beVRdF2cE8w', 
            client_secret='NQtiZSmriDzkW6hY-HaACbG86Nytpw', 
            user_agent='Java tests',
            #password = "no",
            #username="later"
        )

    def search(self,input):
        #problem is that we are relying on reddit sorting system
        # and unrelated post may come up
        # i.e. GPU might come up in a escape from tarkov post

        input = "hololive"
        self.trawler(input)
        for submission in self.reddit.subreddit("all").search(input,'hot',limit=10):
            self.data = Mydata(input)
            self.data.addComment(submission.title)
            iCount = submission.upvote_ratio
            iCount = submission.score/iCount #score if definitly true but the upvote ratio might not be
            iCount *= 100
            self.data.addLikeCount(int(iCount))
        
        #print(block.interactionCount)
        # for c in block.topComments:
        #     print(c)
        
        return self.data
            # print("Title: ",submission.title)
            # print("Author: ",submission.author)
            # print("link: ",submission.permalink)
            # print("updoot: ",submission.score)
            # print("upvote ratio: ",submission.upvote_ratio)
            # print("comment count:",submission.num_comments)
            # commentTree = submission.comments
            # print("comment 1",commentTree[0].body)

    def trawler(self, input):
        # check if there is a related subreddit
        lst = self.reddit.subreddits.search(input,limit=1)
        # c in this case is a subreddit obj
        for c in lst:
            print(c.display_name)
            print(c.subscribers)
            # try:   NEED TO BE A MOD OF THE SUBREDDIT FOR THIS TO WORK
            #     var1=c.traffic() #var1 is a dict obj' IMPORTANT 
            #     print(len(var1))
            #     # varlst = var1["day"] 
            #     # print(varlst[0])
            #     # print(varlst[1])
            #     # print(varlst[2])
            # except prawcore.NotFound:
            #     print("not allowed to view trafic")
        
    
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