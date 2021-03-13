import json
import dateparser as dp
from pathlib import Path


class retrieval:

    def __init__(self):
        pass

    def testData(self,data):
        pass

    def write_json(self, data, filename):
        pass

    def reddit_save(self, searchQuery, rdt_results, queryLimit):
        pass

    def twitter_save(self, searchQuery, tw_results):
        pass


class dataExport(retrieval):
    path = "data/"

    def __init__(self):
        pass

    # function to add to JSON
    def write_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    #save data to file, according to source
    def exportData(self,data):
        data_temp = []
        posts_temp = []
        ids = []

        # Creating directory and file
        p = Path(self.path)
        p.mkdir(parents=True, exist_ok=True)

        topic = str(data[0].topic)
        source = str(data[0].source)
        print(topic, source)
        data_file = self.path + topic + "_" + source + "_data.json"
        posts_file = self.path + topic + "_" + source + "_posts.json"

        # check if file exists
        check_d_file = Path(data_file)
        check_p_file = Path(posts_file)
        if not check_d_file.is_file(): self.write_json(data_temp, data_file)
        if not check_p_file.is_file(): self.write_json(data_temp, posts_file)

        with open(posts_file, 'r') as json_file:
            try:
                cur_data = json.load(json_file)
                posts_temp = cur_data
                for id in posts_temp: ids.append(id['id'])
            except Exception as e:
                print('Exception: ' + str(e))

        id = set(ids)
        for submission in data:
            to_dict = vars(submission)
            d_date = dp.parse(str(to_dict['date']))
            to_dict['date'] = str(d_date)

            tc = submission.getTopComments()
            for posts in tc:
                posts_dict = vars(posts)
                p_date = dp.parse(str(posts_dict['date']))
                posts_dict['date'] = str(p_date)

                if source.lower() in posts_dict['url'].lower() and posts_dict['id'] not in id:
                    #print("found " + source)
                    posts_temp.append(posts_dict)

            if source.lower() == to_dict['source'].lower():
                data_temp.append(to_dict)

        self.write_json(posts_temp, posts_file)
        self.write_json(data_temp, data_file)

    # save reddit data to JSON file
    def reddit_save(self, searchQuery, rdt_results, queryLimit):
        temp = []
        fields = ('id', 'author', 'title', 'url', 'score', 'selftext', 'num_comments', 'created_utc')
        file_name = searchQuery + '_reddit.json'
        reddit_file = Path(file_name)
        if not reddit_file.is_file():
            print("file does not exist, creating temp")  # created due to exception if file does not exist.
            self.write_json(temp, file_name)

        with open(file_name, 'r') as json_file:
            ids = []
            try:
                data = json.load(json_file)
                temp = data
                for id in temp: ids.append(id['id'])
            except Exception as e:
                print('Exception: ' + str(e))

            s = set(ids)

            for submission in rdt_results.hot(limit=5):
                to_dict = vars(submission)
                date = dp.parse(str(to_dict['created_utc']))
                if to_dict['id'] not in s:
                    sub_dict = {field: to_dict[field] for field in fields}
                    sub_dict['author'] = str(submission.author)
                    sub_dict['created_utc'] = str(date)
                    temp.append(sub_dict)

        self.write_json(temp, file_name)

    # save twitter data to JSON file
    def twitter_save(self, searchQuery, tw_results):
        temp = []
        file_name = searchQuery + '_twitter.json'
        twitter_file = Path(file_name)
        if not twitter_file.is_file():
            print("file does not exist, creating temp")  # created due to exception if file does not exist.
            self.write_json(temp, file_name)

        # '''
        with open(file_name, 'r') as json_file:
            ids = []
            try:
                data = json.load(json_file)
                temp = data
                for id in temp: ids.append(id['id'])
            except Exception as e:
                print('Exception: ' + str(e))

            s = set(ids)

            for tweet in tw_results:
                to_dict = vars(tweet)
                date = dp.parse(str(to_dict['created_at']))
                if to_dict['id'] not in s:
                    sub_dict = {}
                    sub_dict['id'] = tweet.id
                    sub_dict['username'] = tweet.user.screen_name
                    sub_dict['created_at'] = str(date)
                    temp.append(sub_dict)

        self.write_json(temp, file_name)
        # '''
