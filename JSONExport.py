import json
import dateparser as dp
from pathlib import Path


class retrieval:

    def __init__(self):
        pass

    def write_json(self, data, filename):
        pass

    def exportData(self, data):
        pass
    
    def combinedData(self, data):
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
        # if not check_d_file.is_file(): self.write_json(data_temp, data_file)
        # if not check_p_file.is_file(): self.write_json(data_temp, posts_file)

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
        
        self.combinedData(data, source, id)
        #self.write_json(posts_temp, posts_file)
        #self.write_json(data_temp, data_file)

    def combinedData(self, data, source, id):
        for submission in data:
            to_dict = vars(submission)
            d_date = dp.parse(str(to_dict['date']))
            to_dict['date'] = str(d_date)
            to_dict['top_comments'] = {}

            tc = submission.getTopComments()
            for posts in tc:
                posts_dict = vars(posts)
                p_date = dp.parse(str(posts_dict['date']))
                posts_dict['date'] = str(p_date)
                top_comments = {}

                if source.lower() in posts_dict['url'].lower() and posts_dict['id'] not in id:
                    #print("found " + source)
                    #posts_temp.append(posts_dict)
                    top_comments.update(posts_dict)
                
                to_dict['top_comments'] = top_comments
            print(to_dict['top_comments'])

            #if source.lower() == to_dict['source'].lower():
                #data_temp.append(to_dict)