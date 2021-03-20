import unittest
import random
import praw
import copy
import mydata
from crawler import redditCrawler,twitterCrawler

class Testcrawler(unittest.TestCase):
    pass

class TestredditCrawler(unittest.TestCase):

    def test_sortTop(self):
        temp3 = []
        reddit = praw.Reddit(
            client_id='zo7beVRdF2cE8w',
            client_secret='NQtiZSmriDzkW6hY-HaACbG86Nytpw',
            user_agent='Java tests'
        )
        testobj1 = praw.models.Submission(reddit,id='kplck8')
        testobj2 = praw.models.Submission(reddit,id='m95lzk')
        testobj3 = praw.models.Submission(reddit,id='m94j1u')
        testobj4 = praw.models.Submission(reddit,id='iuxslh')
        temp3.append(testobj1)
        temp3.append(testobj2)
        temp3.append(testobj3)
        i = redditCrawler()

        low, temp3 = i._sortTop(testobj4,temp3)

        #test the corrent low value return
        self.assertEqual(low, temp3[0].score)
        
        #test the posts are sorted in order
        self.assertGreater(temp3[1].score,temp3[0].score)
        self.assertGreater(temp3[2].score,temp3[1].score)

#     def test_search(self):
#         i = redditCrawler()
#         dat = i.search('anime')
#         #check that the 7 my dataobjs are returned
#         self.assertEqual(len(dat),7)
        
#         #test interaction count
#         count = 0
#         for day in dat:
#             count += day.interactionCount

#         self.assertGreater(count,0)

#         #test comment count
#         comment = 0
#         for day in dat:
#             comment += day.commentCount

#         self.assertIsInstance(day,mydata.Mydata)
#         self.assertGreater(comment,0)

#     def test_generalSearch(self):
#         i = redditCrawler()
#         dat = i.generalSearch('feng shui')
#         #check that the 7 my dataobjs are returned
#         self.assertEqual(len(dat),7)
        
#         #test interaction count
#         count = 0
#         for day in dat:
#             count += day.interactionCount

#         self.assertGreater(count,0)

#         #test comment count
#         comment = 0
#         for day in dat:
#             comment += day.commentCount

#         self.assertIsInstance(day,mydata.Mydata)
#         self.assertGreater(comment,0)
        
        

#     #unable to test format due to how it links to search
#     #self.fail() #use when case fails

# class TesttwitterCrawler(unittest.TestCase):
    
#     def setUp(self):
#         self.t = twitterCrawler()

#     def testResultLength(self):
#         result = self.t.search("covid")
#         self.assertEqual(len(result), 7)

#     def testLikeCount(self):
#         result = self.t.search("covid")

#         likes = 0
#         for day in result:
#             likes += day.interactionCount
#         self.assertGreater(likes,0)

#     def testRetweetCount(self):
#         result = self.t.search("covid")

#         retweets = 0
#         for day in result:
#             retweets += day.commentCount
#         self.assertGreater(retweets,0)

#     def testNoResults(self):
#         result = self.t.search("uighsshhagegerg")
#         tweets = 0

#         for day in result:
#             for tweet in day.topComments:
#                 tweets += 1

#         self.assertEqual(tweets, 0)


if __name__ == '__main__':
    unittest.main()