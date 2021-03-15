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
    
    def searchHist(self, query):
        pass


class dataExport(retrieval):
    path = "data/"
    # Creating directory 'data' for saving JSON files
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    # Seach History file 
    searchHist_file = path + "user_search_hist.json"
    check_hist_file = Path(searchHist_file)

    def __init__(self):
        pass

    # Function to add to JSON
    def write_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    # Function to get user's search history to show on UI
    def getSearchHist(self):
        hist_temp = {}
        hist_arr = []
        
        if self.check_hist_file.is_file():
            with open(self.check_hist_file, 'r') as json_file:
                try:
                    cur_data = json.load(json_file)
                    hist_temp = cur_data
                    if hist_temp: hist_arr = hist_temp['search']

                except Exception as e:
                    print('Get Search History - Exception: ' + str(e))
            
        elif not self.check_hist_file.is_file(): 
            print("Search History file does not exist, creating temp... ")
            self.write_json(hist_temp, self.searchHist_file) #create empty file before adding search query
        
        return hist_arr

    # Function to save user's search query to JSON file
    def addSearchHist(self, query): #add current search query to data file for future reference
        print("query: ", query)
        hist_temp = {}
        hist_arr = []

        with open(self.check_hist_file, 'r') as json_file:
            try:
                cur_data = json.load(json_file)
                hist_temp = cur_data
                if hist_temp: hist_arr = hist_temp['search']
                
                hist_arr.append(query.capitalize())
                
                hist_temp['search'] = hist_arr
            except Exception as e:
                print('Add Search History - Exception: ' + str(e))
        
        self.write_json(hist_temp, self.searchHist_file)

    #save data to file, according to source
    def exportData(self,data):
        data_temp = []
        posts_temp = []
        ids = []

        # Creating directory and file
        p = Path(self.path)
        p.mkdir(parents=True, exist_ok=True)

        topic = str(data[0].topic) # get the topic the user searched for 
        source = str(data[0].source) # get the source (either reddit or twitter)
        print(topic, source) # print for verification
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