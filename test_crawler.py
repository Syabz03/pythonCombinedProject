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

    def test_sortTop(self):
        pass
        #self.fail() #use when case fails

# class TesttwitterCrawler(unittest.TestCase):
#     def test_search(self):
#         self.fail()

#     def test_format(self):
#         self.fail()

if __name__ == '__main__':
    unittest.main()