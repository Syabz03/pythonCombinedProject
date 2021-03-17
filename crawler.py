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
    def search(self, input):
        self.topic = input

    def format(self):
        pass


class redditCrawler(crawler):
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
        # problem is that we are relying on reddit sorting system
        # and unrelated post may come up
        # i.e. GPU might come up in a escape from tarkov post cause of in game item
        super().search(input)

        # V2
        self.topic = input
        multiReddit = self.reddit.subreddits.search(self.topic, limit=5)
        for subr in multiReddit:  # get related subreddits
            print("----------------------------------------------------------------------------")
            print(subr.display_name)
            print(subr.subscribers)
            try:
                # removal of spaces and uppercase alpha as reddit does not allow those in subreddit name
                if self.topic.lower().replace(" ", "") in str(subr.display_name).lower():
                    # if subreddit name contains topic
                    self.subRedditPost.append(subr.top(time_filter='week', limit=100))
                else:
                    # if subreddit name does not contains topic
                    self.subRedditPost.append(subr.search(self.topic, sort='top', time_filter='week', limit=100))
            except:  # supposed to throw specific error but either api or package updated and provided docs no longer correct
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
            except:  # supposed to throw specific error but either api or package updated and docs no longer correct
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

        # get data from the day's post
        # Clears getTopComments list to avoid combining both results
        date = datetime.now() - timedelta(days=n)
        temp = Mydata(self.topic, 'reddit', date)

        if len(temp.getTopComments()) != 0:
            temp.getTopComments().clear()

        for day in week:
            date = datetime.now() - timedelta(days=n)
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
                    day_summary.addLikeCount(int(iCount))
                if (len(top3) < 3) and (not post.over_18):  # so that nsfw stuff does not appear in top posts
                    top3.append(post)
                elif (post.score > low) and (not post.over_18):
                    low, top3 = self.sortTop(post, top3)

            # additon of the top 3 post to the day summary
            for top in top3:
                url = 'reddit.com' + top.permalink
                day_summary.addPost(top.title, top.id, url, top.created_utc)
            self.data.append(day_summary)
        return None

    # to sort out the top 3 posts of the day
    def sortTop(self, post, top3):
        low = 0         

        #add the new post to the list and sort with lowest at the front
        top3.append(post) 
        top3.sort(key=self.getScore)
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

    def getScore(self, n):
        return n.score
    # notes

    # c in this case is a subreddit obj
    # cannot iterate here as the end of the list will be reached
    # for c in lst:
    #     print(c.display_name)
    #     print(c.subscribers)


class twitterCrawler(crawler):

    def __init__(self):
        consumer_key = "VpNVndPOykZXjQgfTg2RD21xz"
        consumer_secret = "1LyM7m5lTmNWwzUUSJF2kN04B5bZvRStY663PjNEnQRCS6b2QW"
        access_token = "1358367734417903620-liyj12fLuUrQGM09nsqiVqiAsFKuRc"
        access_token_secret = "r5O5AQYHDZrddrPki5FKDZUritllO3VRSoCIlHJv84UEA"

        # For OAuth 1a authentication
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  # Creating the authentication object
        self.auth.set_access_token(access_token, access_token_secret)  # Setting your access token and secret

        self.api = tweepy.API(self.auth,
                              wait_on_rate_limit=True)  # Creating the API object while passing in auth information

    def search(self, input):
        self.data = []  # empty data
        self.topic = input

        tweet_limit = 50

        # For loop to change target day, api searches for tweets of the day before
        # The until tag returns tweets created before the given date. I.e. -1 for today, 6 for 6 days before (Total 7 days)
        for n in range(-1, 6):
            day = datetime.now() - timedelta(days=n)
            results = self.api.search(q=f"{input} -filter:replies -filter:retweets", result_type="mixed",
                                      count=tweet_limit, until=day.strftime("%Y-%m-%d"))  # Find tweets for that day

            self.format(results, day)

        # Temp tweet print function
        # print("\n========================================Twitter Result===========================================\n")
        #
        # for n in range(0, 7):
        #
        #    print(f"Day {n+1})\n")
        #
        #    #for i in range(tweet_limit):
        #    #
        #    #    print(self.data[n].topComments[i].text)
        #    #    print(self.data[n].topComments[i].url)
        #    #    print()
        #
        #    print("Total retweets: " + str(self.data[n].commentCount))
        #    print("Total likes: " + str(self.data[n].interactionCount))
        #    print()
        return self.data

    def format(self, block, day):
        # super().format(block)

        temp = Mydata(self.topic, 'Twitter', day)

        #Clears getTopComments list to avoid combining both results
        if len(temp.getTopComments())!=0:
            temp.getTopComments().clear()

        # Go through tweets and combine the interaction data into 1 number for 1 day
        for tweet in block:
            url = f"https://twitter.com/i/web/status/{tweet.id}"
            temp.addPost(tweet.text, tweet.id, url, tweet.created_at)

            # print(tweet.text)
            # print(f"https://twitter.com/i/web/status/{tweet.id}")

            temp.addLikeCount(tweet.favorite_count)
            temp.addCommentCount(tweet.retweet_count)

        self.data.append(temp)
        # Get top 3 post for day
        # Get url