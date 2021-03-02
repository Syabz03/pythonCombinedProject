import tweepy
import praw
import prawcore
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
            client_id='zo7beVRdF2cE8w', 
            client_secret='NQtiZSmriDzkW6hY-HaACbG86Nytpw', 
            user_agent='Java tests',
            password = "no",
            username="later"
        )

    def search(self,input):
        #problem is that we are relying on reddit sorting system
        # and unrelated post may come up
        # i.e. GPU might come up in a escape from tarkov post

        input = "hololive"
        self.trawler(input)
        for submission in self.reddit.subreddit("all").search(input,'hot',limit=10):
            block = Mydata(input)
            block.addComment(submission.title)
            iCount = submission.upvote_ratio
            iCount = submission.score/(iCount-(1-iCount))
            iCount *= 100
            block.addLikeCount(int(iCount))
        
        #print(block.interactionCount)
        # for c in block.topComments:
        #     print(c)
        
        return block
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
            try:
                var1=c.traffic() #var1 is a dict obj' IMPORTANT 
                varlst = var1["day"] 
                print(varlst[1])
            except prawcore.NotFound:
                print("not allowed to view trafic")
                #always throws even when data is correct
        
    
    def format(self, block):
        #return data obj
        pass
