class Mydata:
    topic=''
    source=''
    date=''
    interactionCount=''
    commentCount=''
    topComments=[]

    def __init__(self,topic,platform,date):
        self.topic = topic
        self.source = platform
        self.date = date
        self.interactionCount = 0
        self.commentCount =0
    
    def addPost(self,text,url):
        self.topComments.append(Post(text,url))

    def addLikeCount(self,like):
        self.interactionCount += like
    
    def addCommentCount(self,count):
        self.commentCount += count
        
class Post:
    
    text = ''
    url =''

    def __init__(self,text, url):
        self.text = text
        self.url = url

