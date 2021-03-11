import tweepy
import praw
import prawcore
from abc import ABC, abstractmethod 
from mydata import *
from datetime import datetime, timedelta, date

class crawler(ABC):
    topic = ''
    data = []

    def __init__(self):
        pass

    @abstractmethod
    def search(self,input):
        self.topic = input

    def format(self):
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
        for subr in multiReddit:        #get related subreddits
            print("---------------------------------------------------------------------------------------------------------------")
            print(subr.display_name)
            print(subr.subscribers)
            try:
                if self.topic.lower() in str(subr.display_name).lower():                                        #if subreddit name contains topic
                    print('in if')
                    self.subRedditPost.append(subr.top(time_filter='week',limit=100))
                else:
                    print('in else')
                    self.subRedditPost.append(subr.search(self.topic,sort='top',time_filter='week',limit=100))  #if subreddit name does not contains topic
            except: #supposed to throw specific error but either api or package updated and docs no longer correct
                print("not allowed to view trafic")

        self.format()
        return self.data
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
        # 1 week = 604800
        # 1 day = 86400
        days, day1, day2, day3, day4, day5, day6, day7 = ([] for i in range(8))
        #sort into days of the week
        for postlist in self.subRedditPost:
            print('mark')
            try:
                for submission in postlist:
                    created = submission.created_utc
                    utcTime = datetime.timestamp(datetime.now())
                    if created < (utcTime-(6*86400)):
                        day1.append(submission)
                    elif created < (utcTime-(5*86400)):
                        day2.append(submission)
                    elif created < (utcTime-(4*86400)):
                        day3.append(submission)
                    elif created < (utcTime-(3*86400)):
                        day4.append(submission)
                    elif created < (utcTime-(2*86400)):
                        day5.append(submission)
                    elif created < (utcTime-86400):
                        day6.append(submission)
                    else:
                        day7.append(submission)
            except:  # supposed to throw specific error but either api or package updated and docs no longer correct
                print("not allowed to view trafic")
        days.append(list(day1))  # oldest
        days.append(list(day2))
        days.append(list(day3))
        days.append(list(day4))
        days.append(list(day5))
        days.append(list(day6))
        days.append(list(day7))
        n =0
        for d in days:
            n = n+len(d)
        print(n," post crawled")

        #get data from the day's post
        for day in days:
            print(len(day))
            n = 6
            date = datetime.now() - timedelta(days=n)
            temp = Mydata(self.topic, 'reddit', date)
            top3 = [0,0,0]
            for post in day:
                temp.addPost(post.title,post.permalink)
                iCount = post.upvote_ratio  # PLS FIX
                iCount = iCount - (1-iCount)
                iCount = post.score / (iCount*100)  # score if definitly true but the upvote ratio might not be
                iCount *= 100
                temp.addLikeCount(int(iCount))
            self.data.append(temp)
            n -= 1



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
