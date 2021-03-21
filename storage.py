import json
import dateparser as dp
from pathlib import Path
from datetime import date
import copy

class storage():
    """A class to be called by main.py for exporting of crawled data to a json file

    Attributes:
        path : str
            folder name to be created/searched for storing Reddit & Twitter data files
        p : Path()
            use function Path() for the program to find the path 'path' and return it to variable 'p'
        searchHist_file : str
            file name to be created/searched for storing Reddit & Twitter data
        check_hist_file : str
            use function Path() for the program to find the path 'path'
    
    Methods:
        write_json(data, filename) :
            write values in 'data' to a file with value of 'filename'
        getSearchHist :
            returns user's search history to be displayed on UI 
        addSearchHist(queryList) : 
            receive values in 'queryList' to a dict before writing to a JSON file with 'write_json' method
        exportData(data, topic) :
            function to read values in 'data' and prepare for export to JSON file with 'write_json' method

    """

    # Creating directory 'data' for saving JSON files
    path = "data/"
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    # Seach History file 
    searchHist_file = path + "user_search_hist.json"
    check_hist_file = Path(searchHist_file)

    def write_json(self, data, filename): # Function to add to JSON
        """A function to write data that is passed to the function to a file 

        Args:
            data : dict
                contains the crawled data
            filename: str
                name for the file to be saved as by the program
        
        """

        with open(filename, 'w') as f:
            json.dump(data, f)
    
    def read_json(self, filename):
        """A function to read data from a file that has the given filename

        Args:
            filename : str
                name of file to be read by the program and store the values to variable 'cur_data'
        
        Return:
            cur_data : list
                list of all data in the file
        
        """

        with open(filename, 'r') as json_file:
            cur_data = json.load(json_file)
            return cur_data  

    def getSearchHist(self): # Function to get user's search history from file to show on UI
        """A function to get user's previous searches and return it to the caller (UI)

        Attributes:
            hist_temp : dict
                contains the crawled data
            hist_arr : list
                name for the file to be saved as by the program

        Returns:
            hist_arr : list
                list of past user searches
        
        """

        hist_temp = {}
        hist_arr = []
        
        if self.check_hist_file.is_file():
            try:
                hist_temp = self.read_json(self.check_hist_file)
                if hist_temp: hist_arr = hist_temp['search']

            except Exception as e:
                print('[JSONExport] Get Search History - Exception: ' + str(e))
            
        elif not self.check_hist_file.is_file(): 
            print("No Search History ")
            self.write_json(hist_temp, self.searchHist_file) # Create empty file for future use since does not exist
        
        return hist_arr # Return search history from file 

    def addSearchHist(self, queryList): # Function to save user's search query to JSON file # Add current search query to data file for future reference
        """A function to add new user's search query to file for future retrieval

        Args:
            queryList : list
                list of queries shown on the UI

        Attributes:
            hist_temp : dict
                to store data in queryList as value to a dict key 'search'
        
        """

        hist_temp = {}
        hist_temp['search'] = queryList # Insert list of query from Search History text box to hist_temp dictionary
        self.write_json(hist_temp, self.searchHist_file) # Call write_json function to store items in hist_temp to specified file

    def exportData(self, data, topic): # Save data to file, according to source (Reddit or Twitter)
        """A function to export crawled data to a JSON file

        Args:
            data : dict
                contains the crawled data
            topic : str
                user's current search query

        Attributes:
            data_temp : list
                to store 'Mydata' object's items
            posts_temp : list
                to store all posts that was crawled
            dates_temp : list
                to store all dates of data in the current '_data.json' file (if available) for comparison to insert new entry or not
            ids_temp : list
                to store all ids of posts in the current '_post.json' file (if available) for comparison to insert new entry or not
            source : str
                get the source of the data (either Reddit or Twitter)
            data_file : str 
                name for the file to be saved as by the program
            posts_file : str
                name for the file to be saved as by the program
            check_d_file : Path()
                use function Path() for the program to find the path 'data_file' and return to the variable 'check_d_file'
            check_p_file : Path()
                use function Path() for the program to find the path 'posts_file' and return to the variable 'check_p_file'
        
        """

        dataTemp = copy.deepcopy(data)
        data_temp = []
        posts_temp = []
        dates_temp = [] # store data's dates for comparison to insert new entry or not
        ids_temp = []  # store posts's ids for comparison to insert new entry or not

        source = str(dataTemp[0].source) # get the source (either reddit or twitter)
        print("[STORAGE] Exporting Data: ", topic, " From: ", source) # print for verification
        data_file = self.path + topic + "_" + source + "_data.json" 
        posts_file = self.path + topic + "_" + source + "_posts.json"

        # check if file exists
        check_d_file = Path(data_file)
        check_p_file = Path(posts_file)
        if not check_d_file.is_file(): self.write_json(data_temp, data_file)
        if not check_p_file.is_file(): self.write_json(data_temp, posts_file)

        try:
            cur_data = self.read_json(data_file)
            if cur_data: # iterate through data if the current file has data in it
                for entries in dataTemp: # iterate through crawled data and get new dates crawled
                    entr_dict = vars(entries)
                    dates_temp.append(str(dp.parse(str(entr_dict['date'])).strftime("%d-%m-%Y")))

                dates_set = set(dates_temp)
                dates_temp.clear()
                for d in cur_data: # store old crawled dates to combine with new crawled dates 
                    if d['date'] not in dates_set:
                        data_temp.append(d)
                        dates_temp.append(d['date'])

            cur_posts = self.read_json(posts_file)
            if cur_posts:
                posts_temp = cur_posts
                for ids in posts_temp: ids_temp.append(ids['id'])
        except Exception as e:
            print('[JSONExport] Reading JSON gave Exception: ' + str(e))

        id_set = set(ids_temp)
        date_set = set(dates_temp)
        for submission in dataTemp:
            to_dict = vars(submission)
            if not to_dict['topic']: to_dict['topic'] = topic
            to_dict['date'] = str(dp.parse(str(to_dict['date'])).strftime("%d-%m-%Y"))
            
            if to_dict['date'] not in date_set: # Update JSON file for the dates crawled, keeping previously crawled entries
                top_com_temp = []
                tc = submission.getTopComments()
                
                for posts in tc:
                    posts_dict = vars(posts)
                    posts_dict['date'] = str(dp.parse(str(posts_dict['date'])).strftime("%d-%m-%Y %H:%M:%S"))
                    
                    if source.lower() in posts_dict['url'].lower() and posts_dict['id'] not in id_set:
                        posts_temp.append(posts_dict)
                    
                    top_com_temp.append(posts_dict) 

                top_com = sorted(top_com_temp, key=lambda k: k['date'], reverse=True) # sort top comments by date
                to_dict['topComments'] = top_com

                if source.lower() == to_dict['source'].lower():
                    data_temp.append(to_dict)
        
        posts_ls = sorted(posts_temp, key=lambda k: k['date'], reverse=True) # sort posts by date
        data_ls = sorted(data_temp, key=lambda k: k['date'], reverse=True) # sort data by date
        
        self.write_json(posts_ls, posts_file)
        self.write_json(data_ls, data_file)
