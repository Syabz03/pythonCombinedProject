import tweepy
import praw
import prawcore
from abc import ABC, abstractmethod
from mydata import *
from datetime import datetime, timedelta, date
from urllib import error

class crawler(ABC):

    """A class to be inherited by redditCrawler and twitterCrawler 

    Attributes:
        topic : str
            the topic being crawled
        data : list
            list of 7 mydata obj representing a week crawled
        
    """
    topic = ''
    data = []

    def __init__(self):
        pass

    @abstractmethod
    def search(self, input):
        self.topic = input

    def format(self):
        pass


class redditCrawler(crawler):
    """A class that inherits from the crawler class to search reddit 
    Attributes:
        reddit: obj
            a reddit obj by the praw package
        subRedditPost : list
            A list used to contain the raw data from the praw package

    Methods: 
        search(topic)
            Searches using the reddit API for the past week for the related topic
        
    """

    reddit = ''
    subRedditPost = []

    def __init__(self):
        # setup reddit object
        self.reddit = praw.Reddit(
            client_id='zo7beVRdF2cE8w',
            client_secret='NQtiZSmriDzkW6hY-HaACbG86Nytpw',
            user_agent='Java tests'
        )

    def search(self, input):
        """ Searches using the reddit API for the past week for the related topic
        Args:
            input (str): Topic that will be searched for

        Returns:
            list: a list 7 mydata Objects representing the past week of data on the topic on reddit
        
        Notes:
            we are relying on reddit sorting system therefore unrelated posts might come up
            i.e. "GPU" might come up in a escape from tarkov post cause of an in game item
        """
        super().search(input)
        self.data=[]
        multiReddit = self.reddit.subreddits.search(self.topic, limit=5)
        for subr in multiReddit:  # get related subreddits
            print("----------------------------------------------------------------------------")
            print(subr.display_name)
            print(subr.subscribers)
            try:
                # removal of spaces and uppercase as reddit does not allow those in subreddit name
                if self.topic.lower().replace(" ", "") in str(subr.display_name).lower():
                    # if subreddit name contains topic
                    self.subRedditPost.append(subr.top(time_filter='week', limit=100))
                else:
                    # if subreddit name does not contains topic
                    self.subRedditPost.append(subr.search(self.topic, sort='top', time_filter='week', limit=100))
            except:
                print("not allowed to view trafic")

        self._format()

        return self.data

        # print("Title: ",submission.title)
        # print("Author: ",submission.author)
        # print("link: ",submission.permalink)
        # print("updoot: ",submission.score)
        # print("upvote ratio: ",submission.upvote_ratio)
        # print("comment count:",submission.num_comments)
        # commentTree = submission.comments
        # print("comment 1",commentTree[0].body)

    def generalSearch(self):
        try:
            self.subRedditPost = []

            self.subRedditPost.append(self.reddit.subreddit("all").search(input,'top',limit=100,time_filter='week'))
        except :
            print("not allowed to view trafic")
        self._format()
        return None

    def _format(self):
        # 1 week = 604800
        # 1 day = 86400
        week, day1, day2, day3, day4, day5, day6, day7 = ([] for i in range(8))
        # sort into days of the week
        for postlist in self.subRedditPost:
            try:
                for submission in postlist:
                    # sort the crawled post by days in the past week
                    created = submission.created_utc
                    utcTime = datetime.timestamp(datetime.now())
                    if created < (utcTime - (6 * 86400)):
                        day1.append(submission)
                    elif created < (utcTime - (5 * 86400)):
                        day2.append(submission)
                    elif created < (utcTime - (4 * 86400)):
                        day3.append(submission)
                    elif created < (utcTime - (3 * 86400)):
                        day4.append(submission)
                    elif created < (utcTime - (2 * 86400)):
                        day5.append(submission)
                    elif created < (utcTime - 86400):
                        day6.append(submission)
                    else:
                        day7.append(submission)
            except:
                print("not allowed to view trafic")
        week.append(list(day1))  # oldest
        week.append(list(day2))
        week.append(list(day3))
        week.append(list(day4))
        week.append(list(day5))
        week.append(list(day6))
        week.append(list(day7))
        n = 0
        for d in week:
            n = n + len(d)
        print(n, " post crawled")
        if n == 0:
            self.generalSearch()
            pass

        
        n = 6
        # get data from the day's post
        for day in week:
            date = datetime.now() - timedelta(days=n)
            date = date.strftime("%d-%m-%Y")
            day_summary = Mydata(self.topic, 'reddit', date)
            top3 = []
            low = 0
            for post in day:
                if post.score == 0:
                    day_summary.addLikeCount(0)
                    # in this case we are unable to determine the about of people upvoting or downvoting posts
                else:
                    # get estimated interaction count
                    iCount = post.upvote_ratio
                    iCount = iCount - (1 - iCount)
                    iCount = post.score / (
                                iCount * 100)  # score if definitly true but the upvote ratio might not be due to reddit obsuring data
                    iCount *= 100
                    day_summary.addCommentCount(post.num_comments)
                    day_summary.addLikeCount(int(iCount))
                if (len(top3) < 3) and (not post.over_18):  # so that nsfw stuff does not appear in top posts
                    top3.append(post)
                elif (post.score > low) and (not post.over_18):
                    low, top3 = self._sortTop(post, top3)

            # additon of the top 3 post to the day summary
            for top in top3:
                url = 'reddit.com' + top.permalink
                day_summary.addPost(top.title, top.id, url, top.created_utc)
            self.data.append(day_summary)
            n -= 1
        return None

    # to sort out the top 3 posts of the day
    def _sortTop(self, post, top3):
        low = 0         

        #add the new post to the list and sort with lowest at the front
        top3.append(post) 
        top3.sort(key=self._getScore)
        if len(top3) > 3:
            top3.pop(0)

        #set the lowest score of top 3
        low = top3[0].score
        n = 1
        for top in top3:
            print(n, ". ", top.title)
            print("score: ", top.score)
            n += 1
        return low, top3 # return the lowest score and the list of top3 posts

    def _getScore(self, n):
        return n.score
    # notes

    # c in this case is a subreddit obj
    # cannot iterate here as the end of the list will be reached
    # for c in lst:
    #     print(c.display_name)
    #     print(c.subscribers)


class twitterCrawler(crawler):
    """
    A class that inherits from the crawler class for crawling Twitter

    Attributes
    ----------
    topthree : object list
        
        stores the top three tweets of a day. One element in the list represents a day

    Methods
    -------
    search(input)
        
        searches 50 tweets per day from the past week using the API for the topic given
    """

    topthree = []

    def __init__(self):
        """
        Parameters
        ----------
        consumer_key : str
            
            twitter account key for creating OAuth1a authentication with Twitter
        
        consumer_secret : str
            
            twitter account secret key for creating OAuth1a authentication with Twitter
        
        access_token : str
            
            twitter account access token for generating access token from Twitter
        
        access_token_secret : str
            
            twitter account secret token for generating access token from Twitter
        
        api : API object
            
            stores API object for API methods
        """
        consumer_key = "VpNVndPOykZXjQgfTg2RD21xz"
        consumer_secret = "1LyM7m5lTmNWwzUUSJF2kN04B5bZvRStY663PjNEnQRCS6b2QW"
        access_token = "1358367734417903620-liyj12fLuUrQGM09nsqiVqiAsFKuRc"
        access_token_secret = "r5O5AQYHDZrddrPki5FKDZUritllO3VRSoCIlHJv84UEA"

        # For OAuth 1a authentication
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  # Creating the authentication object
        self.auth.set_access_token(access_token, access_token_secret)  # Setting your access token and secret

        self.api = tweepy.API(self.auth,
                              wait_on_rate_limit=True)  # Creating the API object while passing in auth information

    def search(self,input):
        """
        searches 50 tweets per day from the past week using the API for the topic given
        
        Parameters
        ----------
        input : str
            
            the topic to be searched

        Returns
        -------
        list
            
            a list of size 7 mydata objects containing a list of posts, a total retweet count and a total like count

        Notes
        -----
        the method works by searching a number of tweets of a certain day, however since the API cannot exactly search for a single day, it would add tweets of days up to a week before the specified day if it cannot find enough tweets, hence very popular tweets might come up multiple times
        """
        self.data = []
        self.topic = input

        tweet_limit = 50 #Controls the number of tweets to search for a day

        # For loop to change target day, api searches for tweets
        # The until tag returns tweets created before the given date. I.e. -1 for today, 6 for 6 days before (Total 7 days)
        # Twitter API does not have the ability to search for tweets of a single day, so this method is used to give the closest representation
        for n in range(-1, 6):
            day = datetime.now() - timedelta(days=n)
            results = self.api.search(q=f"{input} -filter:replies -filter:retweets", result_type="mixed", count=tweet_limit, until=day.strftime("%Y-%m-%d")) # Find tweets for that day
            
            # Format the search result block of that day
            self.format(results, day)

        # Print section for checking
        print("\n========================================Twitter Result===========================================\n")
        
        #for n in range(0, 7):
        #
        #    print(f"Day {n+1})\n")
        #
        #    for i in range(len(self.data[n].topComments)):
        #    
        #       print(self.data[n].topComments[i].text)
        #       print(self.data[n].topComments[i].url)
        #       print()
        #
        #    #for j in range(3):
        #    #
        #    #    print("Top tweet: " + str(self.topthree[n].topComments[j].text))
        #
        #
        #    print("Total retweets: " + str(self.data[n].commentCount))
        #    print("Total likes: " + str(self.data[n].interactionCount))
        #    print()
           
        return self.data

    def format(self, block, day):
        """
        takes the results of a particular day and totals the like/retweet counts for that day, while also storing the tweets
        
        Parameters
        ----------
        block : SearchResults object
            
            the block of tweets returned by twitter's API to be looked through

        day : datetime.date

            the date used to search

        Notes
        -----
        the important parameters are added into the data list, while the topthree list is for storing the top three tweets of the particular day
        """
        # super().format(block)

        temp = Mydata(self.topic, 'Twitter', day)
        
        maxlike = [0, 0, 0] # For keeping track of the top three like counts of a day

        #
        #   GENERAL SECTION
        #   For totalling like and comment count
        #

        # Go through tweets and combine the interaction data into 1 number for 1 day
        for tweet in block:
            #url = f"https://twitter.com/i/web/status/{tweet.id}"
            #temp.addPost(tweet.text, tweet.id, url, tweet.created_at)

            temp.addLikeCount(tweet.favorite_count)
            temp.addCommentCount(tweet.retweet_count)

            # Check if the post's like count is higher than the current top three 
            for i in range(len(maxlike)):
                if maxlike[i] < tweet.favorite_count:
                    
                    # After replacing immediately break out, so it does not fill the same value into every element of the array
                    maxlike[i] = tweet.favorite_count
                    break

        #print("MAX LIKE: ")
        #print(maxlike)

        #
        #   SECTION TO FILTER OUT TOP THREE POSTS
        #   Find the top three posts and append to a separate list
        #

        print("\n=====================================================\n")

        #temptop = Mydata(self.topic, 'Twitter', day)
        
        count = 0

        #Only store three tweets
        while count < 3:

            # Go through tweets again to find top three tweets
            for i in maxlike:

                for tweet in block:
                
                    if tweet.favorite_count == i:

                        #print(tweet.text)
                        print(tweet.created_at)

                        url = f"https://twitter.com/i/web/status/{tweet.id}"
                        temp.addPost(tweet.text, tweet.id, url, tweet.created_at)

                        count += 1

                        print("Count:", count)
                    
                    

        self.data.append(temp)
        #self.topthree.append(temptop)
    