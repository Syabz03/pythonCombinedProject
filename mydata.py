class Mydata:
    topic=''
    source=''
    date=''
    interactionCount=''
    commentCount=''
    topComments=''

    def __init__(self,topic,platform,date):
        self.topic = topic
        self.source = platform
        self.date = date
        self.interactionCount = 0
        self.commentCount =0
        self.topComments=[]
    
    def addPost(self,text,id,url,date):
        self.topComments.append(Post(text,id,url,date))

    def addLikeCount(self,like):
        self.interactionCount += like
    
    def addCommentCount(self,count):
        self.commentCount += count

    def getTopComments(self):
        return self.topComments

class Post:
    
    text = ''
    id = ''
    url =''
    date = ''

    def __init__(self, text, id, url, date):
        self.text = text
        self.id = id
        self.url = url
        self.date = date

