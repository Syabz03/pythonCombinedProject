import json
import dateparser as dp
from pathlib import Path

class dataExport():
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

    """A function to write data that is passed to the function to a file 

    Args:
        data : dict
            contains the crawled data
        filename: str
            name for the file to be saved as by the program
    
    """

    def write_json(self, data, filename): # Function to add to JSON
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    """A function to read data from a file that has the given filename

    Args:
        filename : str
            name of file to be read by the program and store the values to variable 'cur_data'
    
    Return:
        cur_data : list
            list of all data in the file
    
    """

    def read_json(self, filename):
        with open(filename, 'r') as json_file:
            cur_data = json.load(json_file)
            return cur_data  

    """A function to get user's previous searches and return it to the caller

    Attributes:
        hist_temp : dict
            contains the crawled data
        hist_arr : list
            name for the file to be saved as by the program

    Returns:
        hist_arr : list
            list of past user searches
    
    """

    def getSearchHist(self): # Function to get user's search history from file to show on UI
        hist_temp = {}
        hist_arr = []
        
        if self.check_hist_file.is_file():
            try:
                hist_temp = self.read_json(self.check_hist_file)
                if hist_temp: hist_arr = hist_temp['search']

            except Exception as e:
                print('Get Search History - Exception: ' + str(e))
            
        elif not self.check_hist_file.is_file(): 
            print("No Search History ")
            self.write_json(hist_temp, self.searchHist_file) # Create empty file for future use since does not exist
        
        return hist_arr # Return search history from file 

    """A function to add new user search to file

    Args:
        queryList : list
            list of queries shown on the UI

    Attributes:
        hist_temp : dict
            to store data in queryList as value to a dict key 'search'
    
    """

    def addSearchHist(self, queryList): # Function to save user's search query to JSON file # Add current search query to data file for future reference
        hist_temp = {}
        hist_temp['search'] = queryList # Insert list of query from Search History text box to hist_temp dictionary
        self.write_json(hist_temp, self.searchHist_file) # Call write_json function to store items in hist_temp to specified file

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
        ids : list
            to store all ids of posts in the current '_post.json' file (if available)
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

    def exportData(self, data, topic): # Save data to file, according to source (Reddit or Twitter)
        data_temp = []
        posts_temp = []
        ids = []
        
        source = str(data[0].source) # get the source (either reddit or twitter)
        # print(topic, source) # print for verification
        data_file = self.path + topic + "_" + source + "_data.json" 
        posts_file = self.path + topic + "_" + source + "_posts.json"

        # check if file exists
        check_d_file = Path(data_file)
        check_p_file = Path(posts_file)
        if not check_d_file.is_file(): self.write_json(data_temp, data_file)
        if not check_p_file.is_file(): self.write_json(data_temp, posts_file)

        try:
            cur_data = self.read_json(posts_file)
            posts_temp = cur_data
            for id in posts_temp: ids.append(id['id'])
        except Exception as e:
            print('Exception: ' + str(e))

        id = set(ids)
        for submission in data:
            to_dict = vars(submission)
            to_dict['date'] = str(dp.parse(str(to_dict['date']))).split()[0]
            top_com = []

            tc = submission.getTopComments()
            for posts in tc:
                posts_dict = vars(posts)
                posts_dict['date'] = str(dp.parse(str(posts_dict['date'])))

                if source.lower() in posts_dict['url'].lower() and posts_dict['id'] not in id:
                    posts_temp.append(posts_dict)
                
                top_com.append(posts_dict) 

            to_dict['topComments'] = top_com

            if source.lower() == to_dict['source'].lower():
                data_temp.append(to_dict)
        
        self.write_json(posts_temp, posts_file)
        self.write_json(data_temp, data_file)
