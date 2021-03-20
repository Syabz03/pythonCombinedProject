import json
import unittest

from storage import storage


class testStorage(unittest.TestCase):
    """A class to test that reading and writing of data to JSON files works as intended

    """

    def test_read_write(self):
        """A function to test writing and reading of sample data using functions in storage.py 

        Attributes:
            de : str
                name of file to be read by the program and store the values to variable 'cur_data'
            sample_json : dict 
                sample json data to be written to a test file and to be used for comparison
            file_name : str
                name of file to be read/write
            json_data : dict
                json data from file name in variable 'file_name' read by function 'read_json'
        
        """
        de = storage()
        sample_json = {
                        "topic": "Hello",
                        "source": "reddit",
                        "date": "2021-12-03",
                        "interactionCount": 1649,
                        "commentCount": 265,
                        "topComments": [
                            {
                                "text": "I guess this makes up for all the times they didn\u2019t give us enough... (4 servings)",
                                "id": "m2bagi",
                                "url": "reddit.com/r/hellofresh/comments/m2bagi/i_guess_this_makes_up_for_all_the_times_they/",
                                "date": "2021-03-11 06:51:18"
                            },
                            {
                                "text": "Just for laughs: today\u2019s garlic (sour cream for scale)",
                                "id": "m36scu",
                                "url": "reddit.com/r/hellofresh/comments/m36scu/just_for_laughs_todays_garlic_sour_cream_for_scale/",
                                "date": "2021-03-12 09:57:54"
                            },
                            {
                                "text": "Just realized that I posted this a year ago and not a single episode has been released since",
                                "id": "m2vmk5",
                                "url": "reddit.com/r/HelloInternet/comments/m2vmk5/just_realized_that_i_posted_this_a_year_ago_and/",
                                "date": "2021-03-12 01:28:10"
                            }
                        ]
                    }
        file_name = 'tests/Hello_data.json'
        de.write_json(sample_json, file_name)
        json_data = de.read_json(file_name)

        self.assertEquals(sample_json,json_data, msg='value is different')

    def test_top_comments_count(self):
        """A function to test that there is 3 data in topComments field of the json data in the file  

        Attributes:
            de : str
                name of file to be read by the program and store the values to variable 'cur_data'
            sample_json : dict 
                sample json data to be written to a test file and to be used for comparison
            file_name : str
                name of file to be read from
            json_data : dict
                json data from file name in variable 'file_name' read by function 'read_json'
            tcLength : int 

        """

        de = storage()
        file_name = 'tests/Hello_data.json'
        json_data = de.read_json(file_name)
        tcLength = len(json_data['topComments'])

        self.assertEquals(tcLength,3, msg='length is not 3')

    def test_url_and_source(self):
        """A function to test that 'source' and 'url' field of the json data in the file tallies 

        Attributes:
            de : str
                name of file to be read by the program and store the values to variable 'cur_data'
            sample_json : dict 
                sample json data to be written to a test file and to be used for comparison
            file_name : str
                name of file to be read from
            json_data : dict
                json data from file name in variable 'file_name' read by function 'read_json'
            tcLength : int 
        
        Notes:
            Example: source - twitter, thus url should contain twitter value.

        """

        de = storage()
        file_name = 'tests/Hello_data.json'
        json_data = de.read_json(file_name)
        source = json_data['source'] + '.com'
        url = json_data['topComments'][0]['url']

        self.assertIn(source, url, msg='Post is from a different source!')

if __name__ == '__main__':
    unittest.main()
