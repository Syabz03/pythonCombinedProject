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
