import unittest
from crawler import redditCrawler,twitterCrawler

class Testcrawler(unittest.TestCase):
    pass

class TestredditCrawler(unittest.TestCase):
    def test_search(self):
        i = redditCrawler()
        dat = i.search('feng shui')

        self.assertEqual(len(dat),7)
        count = 0
        for day in dat:
            count += day.interactionCount

        self.assertGreater(count,0)

    #unable to test format due to how it links to search
    #self.fail() #use when case fails

class TesttwitterCrawler(unittest.TestCase):
    
    def setUp(self):
        self.t = twitterCrawler()

    def testResultLength(self):
        result = self.t.search("covid")
        self.assertEqual(len(result), 7)

    def testLikeCount(self):
        result = self.t.search("covid")

        likes = 0
        for day in result:
            likes += day.interactionCount
        self.assertGreater(likes,0)

    def testRetweetCount(self):
        result = self.t.search("covid")

        retweets = 0
        for day in result:
            retweets += day.commentCount
        self.assertGreater(retweets,0)

    def testNoResults(self):
        result = self.t.search("uighsshhagegerg")
        tweets = 0

        for day in result:
            for tweet in day.topComments:
                tweets += 1

        self.assertEqual(tweets, 0)


if __name__ == '__main__':
    unittest.main()