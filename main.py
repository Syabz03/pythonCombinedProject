import tkinter as tk
import tkinter.ttk as ttk
import tweepy
import praw
#from mydata import *
from crawler import *
from JSONExport import *
import sys
import myPage_support
queryLimit = 5

#Twitter
#consumer_key = "VpNVndPOykZXjQgfTg2RD21xz"
#consumer_secret = "1LyM7m5lTmNWwzUUSJF2kN04B5bZvRStY663PjNEnQRCS6b2QW"
#access_token = "1358367734417903620-liyj12fLuUrQGM09nsqiVqiAsFKuRc"
#access_token_secret = "r5O5AQYHDZrddrPki5FKDZUritllO3VRSoCIlHJv84UEA"
#
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Creating the authentication object
#auth.set_access_token(access_token, access_token_secret) # Setting your access token and secret
#api = tweepy.API(auth,wait_on_rate_limit=True) # Creating the API object while passing in auth information

# c = redditCrawler()
# rdata = c.search("HoLoLiVe")
# de = dataExport()
# de.exportData(rdata)
#
# t = twitterCrawler()
# tdata = t.search("hololive")
# de.exportData(tdata)

#START OF GUI
def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    myPage_support.init(root, top)
    root.mainloop()
w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    myPage_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("821x540+695+284")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("VanillaCast Web Crawler")
        top.configure(background="#f4efe3", highlightbackground="#d9d9d9", highlightcolor="black")

        self.txtSearchHistory = tk.Text(top)
        self.txtSearchHistory.place(relx=0.012, rely=0.278, relheight=0.631, relwidth=0.185)
        self.txtSearchHistory.configure(background="white", font="TkTextFont", foreground="black", highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black", selectbackground="blue", selectforeground="white", wrap="word")
        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.012, rely=0.222, height=25, width=142)
        self.Label1.configure(activebackground="#f9f9f9", activeforeground="black", background="#f4efe3", font="-family {Segoe UI Black} -size 10 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", text='''Search History''')

        self.txtInterCount = tk.Text(top)
        self.txtInterCount.place(relx=0.219, rely=0.296, relheight=0.143, relwidth=0.357)
        self.txtInterCount.configure(background="white", font="TkTextFont", foreground="black", highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black", wrap="word")

        self.graphCanvas = tk.Canvas(top)
        self.graphCanvas.place(relx=0.219, rely=0.519, relheight=0.389, relwidth=0.352)
        self.graphCanvas.configure(background="#ffffff", borderwidth="2", highlightbackground="#f2f0ce", highlightcolor="black", insertbackground="black", relief="ridge", selectbackground="blue", selectforeground="white")

        self.txtReddit = tk.Text(top)
        self.txtReddit.place(relx=0.597, rely=0.093, relheight=0.35, relwidth=0.39)
        self.txtReddit.configure(background="white",font="TkTextFont",foreground="black",highlightbackground="#d9d9d9",highlightcolor="black",insertbackground="black",selectbackground="blue",selectforeground="white",wrap="word")

        self.txtTwitter = tk.Text(top)
        self.txtTwitter.place(relx=0.597, rely=0.519, relheight=0.389, relwidth=0.39)
        self.txtTwitter.configure(background="white",font="TkTextFont",foreground="black",highlightbackground="#d9d9d9",highlightcolor="black",insertbackground="black",selectbackground="blue",selectforeground="white",wrap="word")

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.28, rely=0.241, height=25, width=197)
        self.Label2.configure(activebackground="#f9f9f9",activeforeground="black",background="#f4efe3",disabledforeground="#a3a3a3",font="-family {Segoe UI Black} -size 10 -weight bold",foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black",text='''Interaction Count''')

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.592, rely=0.044, height=25, width=327)
        self.Label3.configure(activebackground="#f9f9f9",activeforeground="black",background="#ffa4a4",disabledforeground="#a3a3a3",font="-family {Segoe UI Black} -size 10 -weight bold",foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black",text='''Reddit''')

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.597, rely=0.463, height=25, width=317)
        self.Label4.configure(activebackground="#f9f9f9",activeforeground="black",background="#e3f8fb",disabledforeground="#a3a3a3",font="-family {Segoe UI Black} -size 10 -weight bold",foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black",text='''Twitter''')

        self.Label5 = tk.Label(top)
        self.Label5.place(relx=0.341, rely=0.463, height=25, width=88)
        self.Label5.configure(activebackground="#f9f9f9",activeforeground="black",background="#f4efe3",disabledforeground="#a3a3a3",font="-family {Segoe UI Black} -size 10 -weight bold",foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black",text='''Graph''')

        self.txtSearch = tk.Entry(top)
        self.txtSearch.place(relx=0.012, rely=0.019, relheight=0.076, relwidth=0.403)

        self.btnSearch = tk.Button(top)
        self.btnSearch.place(relx=0.426, rely=0.019, height=44, width=87)
        self.btnSearch.configure(activebackground="#fafeda",activeforeground="#000000",background="#f4ecbd",disabledforeground="#a3a3a3",font="-family {Segoe UI Black} -size 10 -weight bold",foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black",pady="0",text='''Search''')

        self.btnQuit = tk.Button(top)
        self.btnQuit.place(relx=0.914, rely=0.926, height=24, width=47)
        self.btnQuit.configure(activebackground="#ececec",activeforeground="#000000",background="#f2bfcd",disabledforeground="#a3a3a3",font="-family {Segoe UI Black} -size 10 -weight bold",foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black",pady="0",text='''Quit''')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.btnSearch.configure(command=lambda:show_entry_fields(self))
        self.btnQuit.configure(command=root.quit)

        showSearchHistory(self)

#END OF GUI

#Reddit
reddit = praw.Reddit(client_id='PESO3cS0KquaWQ', client_secret='ALSLenkZwZ5WCZ-32MaziUw-O7tmeA', user_agent='VanillaCast')

def show_entry_fields(self):
    strVal = self.txtTwitter.get("1.0", 'end')
    if (strVal.strip()):
        self.txtTwitter.delete("1.0", 'end')

    queryVal = self.txtSearch.get() #"Query: %s" % (self.txtSearch.get())
    self.txtTwitter.insert(tk.END, queryVal)

    #query = e1.get() + " -filter:retweets" # The search term you want to find
    #language = "en" #language
    #results = api.search(q=query, lang=language, rpp=queryLimit) #initiate API call

    #for tweet in results: # iterate through every tweets pulled
    #    # printing the text stored inside the tweet object
    #    e3.insert(tk.END, "\n\n")
    #    e3.insert(tk.END, "User: " + tweet.user.screen_name)
    #    e3.insert(tk.END, "\n")
    #    e3.insert(tk.END, "Tweeted: \n")
    #    e3.insert(tk.END, tweet.text)
    #    e3.insert(tk.END, "\n------------------------------------------------")

    redditCrawl(self)
    saveQuery(self, queryVal)

def redditCrawl(self):
    str3Val = self.txtReddit.get("1.0", 'end')
    if (str3Val.strip()):
        self.txtReddit.delete("1.0", 'end')

    ml_subreddit = reddit.subreddit(self.txtSearch.get())

    for post in ml_subreddit.hot(limit=queryLimit):
        self.txtReddit.insert(tk.END, "\n\n")
        self.txtReddit.insert(tk.END, "SubReddit: " + str(post.author))
        self.txtReddit.insert(tk.END, "\n")
        self.txtReddit.insert(tk.END, "Posted: \n")
        self.txtReddit.insert(tk.END, post.title)
        self.txtReddit.insert(tk.END, "\n")
        self.txtReddit.insert(tk.END, "Description: \n")
        self.txtReddit.insert(tk.END, post.selftext)
        self.txtReddit.insert(tk.END, "\n------------------------------------------------")

def showSearchHistory(self):
    field = self.txtSearchHistory
    de = dataExport()
    hist = de.getSearchHist()

    strVal = field.get("1.0", 'end')
    if (strVal.strip()): field.delete("1.0", 'end')
    
    if hist:
        for items in hist:
            field.insert(tk.END, items + "\n")
    field.config(state='disabled')

def saveQuery(self, query):
    items_temp = []
    field = self.txtSearchHistory # Initialise Search History textbox as 'field'
    field.config(state='normal') # Enable 'field' for editing (removing and adding texts)
    index = 1

    # Iterate through 'field' to check if query made matches previous searches
    for item in field.get("1.0", 'end').splitlines():
        if item: 
            if str(item).lower() == query.lower():
                field.delete(str(index) + '.0', str(index) + '.end + 1 char') # Remove text from 'field' if matches with current query
        index += 1

    self.txtSearchHistory.insert('1.0', query.capitalize() + "\n") #Insert current query to first line of 'field'
    field.config(state='disabled') # Disable user from changing 'field' text box
    
    # Get updated search history to store in file
    for item in field.get("1.0", 'end').splitlines():
        if item: items_temp.append(item)

    # Store queries (past and current) to file
    de = dataExport()
    de.addSearchHist(items_temp)
    
if __name__ == '__main__':
    vp_start_gui()
