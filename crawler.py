import tweepy
import praw

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
            client_id='PESO3cS0KquaWQ', client_secret='ALSLenkZwZ5WCZ-32MaziUw-O7tmeA', user_agent='VanillaCast'
        )

    def search(self,input):
        input = "GPU"
        for submission in self.reddit.subreddit("all").search(input,'hot',limit=5):
            print("Title: ",submission.title)
            print("Author: ",submission.author)
            print("link: ",submission.permalink)
            print("updoot: ",submission.score)
    
    def format(self, block):
        #return data obj
        pass
