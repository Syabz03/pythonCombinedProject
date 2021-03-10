import tweepy
import praw
import prawcore
from abc import ABC, abstractmethod 
from mydata import *
from datetime import datetime, timedelta, date

class crawler():
    data =''
    topic = ''

    def search(self,input):
        self.topic = input

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
        super().search(input)

        #V1
        for submission in self.reddit.subreddit("all").search(self.topic,'top',limit=1):
            self.data = Mydata(input)
            self.data.addComment(submission.title)
            iCount = submission.upvote_ratio
            iCount = submission.score/iCount #score if definitly true but the upvote ratio might not be
            iCount *= 100
            self.data.addLikeCount(int(iCount))

        #V2
        self.topic = input
        multiReddit = self.reddit.subreddits.search(self.topic,limit=5)
        for subr in multiReddit:
            print("---------------------------------------------------------------------------------------------------------------")
            print(subr.display_name)
            print(subr.subscribers)
            self.trawl(subr)

        # c in this case is a subreddit obj
        # cannot iterate here as the end of the list will be reached
        # for c in lst:
        #     print(c.display_name)
        #     print(c.subscribers)

        print(len(self.data.topComments))
        return self.data


    def trawl(self,sreddit):
        # check if there is a related subreddit
        
        #pseudo 
        if self.topic.lower() in str(sreddit.display_name).lower():
            print('in if')
            for post in sreddit.top(time_filter='week',limit=100):
                print(post.title)
                self.data.addComment(post.title)
                iCount = post.upvote_ratio
                iCount = post.score/iCount #score if definitly true but the upvote ratio might not be
                iCount *= 100
                self.data.addLikeCount(int(iCount))

        else:
            print('in else')
            for post in sreddit.search(self.topic,sort='top',time_filter='week',limit=100):
                print(post.title)
                self.data.addComment(post.title)
                iCount = post.upvote_ratio
                iCount = post.score/iCount #score if definitly true but the upvote ratio might not be
                iCount *= 100
                self.data.addLikeCount(int(iCount))

        # c in this case is a subreddit obj
        
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


    #notes and extra code
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

    def __init__(self):
        consumer_key = "VpNVndPOykZXjQgfTg2RD21xz"
        consumer_secret = "1LyM7m5lTmNWwzUUSJF2kN04B5bZvRStY663PjNEnQRCS6b2QW"
        access_token = "1358367734417903620-liyj12fLuUrQGM09nsqiVqiAsFKuRc"
        access_token_secret = "r5O5AQYHDZrddrPki5FKDZUritllO3VRSoCIlHJv84UEA"

        # For OAuth 1a authentication
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret) # Creating the authentication object
        self.auth.set_access_token(access_token, access_token_secret) # Setting your access token and secret

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True) # Creating the API object while passing in auth information

    def search(self,input):
        
        #self.data = Mydata(input)

        # Temp variables to hold everything, change when needed
        tweets = []
        total_likes = []
        total_retweets = []

        tweet_limit = 50

        # For loop to change target day, api searches for tweets of the day before
        # The until tag returns tweets created before the given date. I.e. -1 for today, 6 for 6 days before (Total 7 days)
        for n in range(-1, 6):
            day = datetime.now() - timedelta(days=n)
            results = self.api.search(q=f"{input} -filter:retweets", result_type="mixed", count=tweet_limit, until=day.strftime("%Y-%m-%d")) # Find tweets for that day
            
            likes = 0
            retweets = 0

            # Go through tweets 
            for tweet in results:
                tweets.append(tweet.text)
                likes += tweet.favorite_count
                #print(tweet.text + "\n" + str(tweet.favorite_count) + "\n\n")
                retweets += tweet.retweet_count
            
            total_likes.append(likes)
            total_retweets.append(retweets)

        #30-50 tweets per day
        #Get top tweets and combine the interaction data into 1 number for 1 day

        # Temp tweet print function
        print("\n========================================Twitter Result===========================================\n")
        
        for n in range(0, 7):
            
            print(f"Day {n+1})\n")

            #for i in range(tweet_limit):
            #    
            #    print(str(i + n*(tweet_limit) + 1) + ")\n" + tweets[i + n*(tweet_limit)] + "\n")
            
            print("Total retweets: " + str(total_retweets[n]))
            print("Total likes: " + str(total_likes[n]))
            print()

        #return results

    def format(self, block):
        return super().format(block)