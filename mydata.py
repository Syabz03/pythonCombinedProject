class Mydata:
    topic=''
    interactionCount=''
    commentCount=''
    topComments=[]

    def __init__(self,topic):
        self.topic = topic
        self.interactionCount = 0
        self.commentCount =0
    
    def addComment(self,comment):
        self.topComments.append(comment)

    def addLikeCount(self,like):
        self.interactionCount += like
    
    def addCommentCount(self,count):
        self.commentCount += count
        
        
