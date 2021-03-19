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
    
    def test_search(self):
        t = twitterCrawler()
        result = t.search("covid")

        self.assertEqual(len(result), 7)

        likes = 0
        for day in result:
            likes += day.interactionCount

        self.assertGreater(likes,0)

        result2 = t.search("fafoiguauga")
        tweets = 0

        for day in result2:
            for tweet in day.topComments:
                tweets += 1

        self.assertEqual(tweets, 0)


if __name__ == '__main__':
    unittest.main()