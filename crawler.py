import tweepy
import praw
import prawcore
from abc import ABC, abstractmethod 
from mydata import *

class crawler(ABC):
    topic = ''
    data = []

    def __init__(self):
        pass

    @abstractmethod
    def search(self,input):
        self.topic = input

    def format(self, block):
        pass

    
class redditCrawler(crawler):
    reddit=''
    subRedditPost = []

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
        super().search(input)

        #V2
        self.topic = input
        multiReddit = self.reddit.subreddits.search(self.topic,limit=5)
        for subr in multiReddit:
            print("---------------------------------------------------------------------------------------------------------------")
            print(subr.display_name)
            print(subr.subscribers)
            try:
                if self.topic.lower() in str(sreddit.display_name).lower():
                    print('in if')
                    self.subRedditPost.append(sreddit.top(time_filter='week',limit=100))
                else:
                    print('in else')
                    self.subRedditPost.append(sreddit.search(self.topic,sort='top',time_filter='week',limit=100))
            except:
                print("not allowed to view trafic")

        self.format()
        # c in this case is a subreddit obj
        
            # print("Title: ",submission.title)
            # print("Author: ",submission.author)
            # print("link: ",submission.permalink)
            # print("updoot: ",submission.score)
            # print("upvote ratio: ",submission.upvote_ratio)
            # print("comment count:",submission.num_comments)
            # commentTree = submission.comments
            # print("comment 1",commentTree[0].body)


    
    def format(self):
        #return data obj
        #sort here
        

    #notes and extra code

    # for post in sreddit.top(time_filter='week',limit=100):
    #     print(post.title)
    #     self.data.addComment(post.title)
    #     iCount = post.upvote_ratio
    #     iCount = post.score/iCount #score if definitly true but the upvote ratio might not be
    #     iCount *= 100
    #     self.data.addLikeCount(int(iCount))

    # c in this case is a subreddit obj
    # cannot iterate here as the end of the list will be reached
    # for c in lst:
    #     print(c.display_name)
    #     print(c.subscribers)

    # lst = self.reddit.subreddits.search(self.topic,limit=5)
    #     # c in this case is a subreddit obj
    #     for c in lst:
    #         print(c.display_name)
    #         print(c.subscribers)
    #         try:   NEED TO BE A MOD OF THE SUBREDDIT FOR THIS TO WORK
    #             var1=c.traffic() #var1 is a dict obj' IMPORTANT 
    #             print(len(var1))
    #             # varlst = var1["day"] 
    #             # print(varlst[0])
    #             # print(varlst[1])
    #             # print(varlst[2])
    #         except prawcore.NotFound:
    #             print("not allowed to view trafic")
    #     return lst

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