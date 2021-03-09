import json
import dateparser as dp
from pathlib import Path

# function to add to JSON
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

#save reddit data to JSON file
def reddit_save(searchQuery, rdt_results, queryLimit):
    temp = []
    fields = ('id', 'author', 'title', 'url', 'score', 'selftext', 'num_comments', 'created_utc')
    file_name = searchQuery + '_reddit.json'
    reddit_file = Path(file_name)
    if not reddit_file.is_file():
        print("file does not exist, creating temp")  # created due to exception if file does not exist.
        write_json(temp, file_name)

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

    write_json(temp, file_name)

#save twitter data to JSON file
def twitter_save(searchQuery, tw_results):
    temp = []
    file_name = searchQuery + '_twitter.json'
    twitter_file = Path(file_name)
    if not twitter_file.is_file():
        print("file does not exist, creating temp") #created due to exception if file does not exist.
        write_json(temp, file_name)

    #'''
    with open(file_name, 'r') as json_file:
        ids = []

        try:
            data = json.load(json_file)
            temp = data
            for id in temp: ids.append(id['id'])
        except Exception as e:
            print('Exception: '+ str(e))

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

    write_json(temp, file_name)
    #'''