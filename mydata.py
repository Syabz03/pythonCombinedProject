class Mydata:
    """Represents 1 day of data from Reddit or Twitter 
    Attributes:
        topic: str
            Topic being searched
        source : str
            "reddit" or "twitter"
        date: datetime
            The day which the data is for
        interactionCount: int
            number of upvotes/downvotes, likes
        commentCount: int
            number of comments for the day
        topComments: List
            3 of the top posts/tweets for the day

    Methods: 
        __init__(topic, platform, date):
            class constructor
        addPost(text,id,url,date)
            addition of a top 3 post to the day
        addLikeCount(count)
            cummulative addition to the interactionCount
        addCommentCount(count)
            cummulative addition to the commentCount
        getTopComments()
            returns the list of top comments
        
    """
    topic=''
    source=''
    date=''
    interactionCount=''
    commentCount=''
    topComments=''

    def __init__(self,topic,platform,date):
        """class constructor
        Args:
            topic(str): topic that was searched for
            platform(str): "reddit" or "twitter"
            date(datetime): date of the search
        
        Returns:
            mydata class obj   
        """
        self.topic = topic
        self.source = platform
        self.date = date
        self.interactionCount = 0
        self.commentCount =0
        self.topComments=[]
    
    def addPost(self,text,id,url,date):
        """addition of a top 3 post to the day
        A post obj is created then added to the list

        Args:
            text(str): title of the post(reddit) or content of the tweet
            id(str): the unique platform id of the post/tweet
            url(str): url link to the post
            date(datetime): date of the post
        """
        self.topComments.append(Post(text,id,url,date))
        return None

    def addLikeCount(self,count):
        """cummulative addition to the interactionCount

        Args:
            count(int): amount of interactions to be added
        """
        self.interactionCount += count
        return None
    
    def addCommentCount(self,count):
        """cummulative addition to the commentCount
        Args:
            count(int): amount of comments to be added
        """
        self.commentCount += count
        return None

    def getTopComments(self):
        """returns the list of top tweets/posts
        Returns:
            list: a list of 3 top tweets/posts
        """
        return self.topComments

class Post:
    """Represents 1 post/tweet
    Attributes:
        text(str): tweet/post content
        id(str): platform identifier for the post
        url(str): link to the post
        date(datetime): date of the post
    """
    text = ''
    id = ''
    url =''
    date = ''

    def __init__(self, text, id, url, date):
        """class constructor
            Args:
                text(str): tweet/post content
                id(str): platform identifier for the post
                url(str): link to the post
                date(datetime): date of the post
            
            Returns:
                Post class obj   
        """
        self.text = text
        self.id = id
        self.url = url
        self.date = date

    def getText(self):
        """returns the post text
        Returns:
            string: the post text
        """
        return self.text

    def getUrl(self):
        """returns the post url
        Returns:
            string: the post url
        """
        return self.url

    def getDate(self):
        """returns the created date of post
        Returns:
            date: the created date of post
        """
        return self.date
