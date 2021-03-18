import tkinter as tk
import tkinter.ttk as ttk
import tweepy
import praw
# from mydata import *
from crawler import *
from JSONExport import *
import sys
import myPage_support
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

queryLimit = 5

# Twitter
# consumer_key = "VpNVndPOykZXjQgfTg2RD21xz"
# consumer_secret = "1LyM7m5lTmNWwzUUSJF2kN04B5bZvRStY663PjNEnQRCS6b2QW"
# access_token = "1358367734417903620-liyj12fLuUrQGM09nsqiVqiAsFKuRc"
# access_token_secret = "r5O5AQYHDZrddrPki5FKDZUritllO3VRSoCIlHJv84UEA"
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Creating the authentication object
# auth.set_access_token(access_token, access_token_secret) # Setting your access token and secret
# api = tweepy.API(auth,wait_on_rate_limit=True) # Creating the API object while passing in auth information

# c = redditCrawler()
# rdata = c.search("HoLoLiVe")
# de = dataExport()
# de.exportData(rdata)
#
# t = twitterCrawler()
# tdata = t.search("hololive")
# de.exportData(tdata)

# START OF GUI
def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    myPage_support.init(root, top)
    root.mainloop()

w = None

def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
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
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("821x540+695+284")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1, 1)
        top.title("VanillaCast Web Crawler")
        top.configure(background="#f4efe3", highlightbackground="#d9d9d9", highlightcolor="black")

        self.txtSearchHistory = tk.Text(top)
        self.txtSearchHistory.place(relx=0.012, rely=0.278, relheight=0.631, relwidth=0.185)
        self.txtSearchHistory.configure(background="white", font="TkTextFont", foreground="black",
                                        highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black",
                                        selectbackground="blue", selectforeground="white", wrap="word")
        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.012, rely=0.222, height=25, width=142)
        self.Label1.configure(activebackground="#f9f9f9", activeforeground="black", background="#f4efe3",
                              font="-family {Segoe UI Black} -size 10 -weight bold", foreground="#000000",
                              highlightbackground="#d9d9d9", highlightcolor="black", text='''Search History''')

        self.lblReddit = tk.Label(top)
        self.lblReddit.place(relx=0.219, rely=0.222, height=27, width=284)
        self.lblReddit.configure(activebackground="#f9f9f9",activeforeground="black",anchor='n',
                                 background="#ffa4a4",disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI Black} -size 10 -weight bold", foreground="#000000",
                                 highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblReddit.configure(text='''Reddit''')

        self.lblTwitter = tk.Label(top)
        self.lblTwitter.place(relx=0.219, rely=0.352, height=27, width=283)
        self.lblTwitter.configure(activebackground="#f9f9f9",activeforeground="black",anchor='n',
                                  background="#7ddeec",disabledforeground="#a3a3a3",
                                  font="-family {Segoe UI Black} -size 10 -weight bold",
                                  foreground="#000000",highlightbackground="#d9d9d9",
                                  highlightcolor="black")
        self.lblTwitter.configure(text='''Twitter''')

        self.lblComments = tk.Label(top)
        self.lblComments.place(relx=0.219, rely=0.259, height=21, width=284)
        self.lblComments.configure(anchor='nw',background="#ffc4c4",disabledforeground="#a3a3a3",foreground="#000000")
        self.lblComments.configure(text='''Comments: -''')

        self.lblRetweets = tk.Label(top)
        self.lblRetweets.place(relx=0.219, rely=0.389, height=21, width=283)
        self.lblRetweets.configure(activebackground="#f9f9f9",activeforeground="black",anchor='nw',background="#b9edf4",
                                   disabledforeground="#a3a3a3",foreground="#000000",
                                   highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblRetweets.configure(text='''Retweets: -''')

        self.lblUpvotes = tk.Label(top)
        self.lblUpvotes.place(relx=0.219, rely=0.296, height=21, width=284)
        self.lblUpvotes.configure(activebackground="#f9f9f9",activeforeground="black",anchor='nw',
                                  background="#ffc4c4",disabledforeground="#a3a3a3",
                                  font="-family {Segoe UI} -size 9",foreground="#000000",
                                  highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblUpvotes.configure(text='''Upvotes: -''')

        self.lblLikes = tk.Label(top)
        self.lblLikes.place(relx=0.219, rely=0.426, height=21, width=283)
        self.lblLikes.configure(activebackground="#f9f9f9",activeforeground="black",
                                anchor='nw',background="#b9edf4",disabledforeground="#a3a3a3",
                                foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblLikes.configure(text='''Likes: -''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.28, rely=0.167, height=25, width=197)
        self.Label2.configure(activebackground="#f9f9f9", activeforeground="black", background="#f4efe3",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 10 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Interaction Count''')

        #self.graphCanvas = FigureCanvasTkAgg(fig, top)
        #self.graphCanvas.place(relx=0.219, rely=0.519, relheight=0.389, relwidth=0.352)
        # self.graphCanvas.configure(background="#ffffff", borderwidth="2", highlightbackground="#f2f0ce",
        #                            highlightcolor="black", insertbackground="black", relief="ridge",
        #                            selectbackground="blue", selectforeground="white")
        self.figure = Figure(figsize=(5, 4), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.figure, master=top)
        self.canvas.get_tk_widget().place(relx=0.219, rely=0.519, relheight=0.389, relwidth=0.352)


        self.Label5 = tk.Label(top)
        self.Label5.place(relx=0.341, rely=0.478, height=25, width=88)
        self.Label5.configure(activebackground="#f9f9f9", activeforeground="black", background="#f4efe3",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 10 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Graph''')

        self.txtReddit = tk.Text(top, state='disabled')
        self.txtReddit.place(relx=0.597, rely=0.093, relheight=0.35, relwidth=0.39)
        self.txtReddit.configure(background="white", font="TkTextFont", foreground="black",
                                 highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black",
                                 selectbackground="blue", selectforeground="white", wrap="word")

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.597, rely=0.037, height=25, width=320)
        self.Label3.configure(activebackground="#f9f9f9", activeforeground="black", background="#ffa4a4",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 10 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Reddit''')

        self.txtTwitter = tk.Text(top, state='disabled')
        self.txtTwitter.place(relx=0.597, rely=0.519, relheight=0.389, relwidth=0.39)
        self.txtTwitter.configure(background="white", font="TkTextFont", foreground="black",
                                  highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black",
                                  selectbackground="blue", selectforeground="white", wrap="word")

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.597, rely=0.463, height=25, width=317)
        self.Label4.configure(activebackground="#f9f9f9", activeforeground="black", background="#e3f8fb",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 10 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Twitter''')

        self.txtSearch = tk.Entry(top)
        self.txtSearch.place(relx=0.012, rely=0.019, relheight=0.076, relwidth=0.403)

        self.btnSearch = tk.Button(top)
        self.btnSearch.place(relx=0.426, rely=0.019, height=44, width=87)
        self.btnSearch.configure(activebackground="#fafeda", activeforeground="#000000", background="#f4ecbd",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 10 -weight bold",
                                 foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Search''')

        self.btnQuit = tk.Button(top)
        self.btnQuit.place(relx=0.914, rely=0.926, height=24, width=47)
        self.btnQuit.configure(activebackground="#ececec", activeforeground="#000000", background="#f2bfcd",
                               disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 10 -weight bold",
                               foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                               text='''Quit''')

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.btnSearch.configure(command=lambda: show_entry_fields(self))
        self.btnQuit.configure(command=root.quit)

        showSearchHistory(self)

        self.sysLabel = tk.Label(top)
        self.sysLabel.place(relx=0.012, rely=0.111, height=21, width=334)
        self.sysLabel.configure(activebackground="#f9f9f9", activeforeground="black",anchor='w',background="#f4efe3",
                                disabledforeground="#a3a3a3",font="-family {Segoe UI} -size 9 -slant italic",
                                foreground="#eb3034",highlightbackground="#d9d9d9",highlightcolor="black",justify='left')

        self.cBoxGraph = ttk.Combobox(top, state='readonly') #PLACEHOLDER
        self.cBoxGraph.place(relx=0.219, rely=0.926, relheight=0.039, relwidth=0.074)
        self.cBoxGraph.configure(takefocus="")
        self.cBoxGraph.bind("<<ComboboxSelected>>", lambda _: displayDay(self))

        self.gphLabel = tk.Label(top)
        self.gphLabel.place(relx=0.305, rely=0.926, height=21, width=353)
        self.gphLabel.configure(anchor='w',background="#f4efe3",disabledforeground="#a3a3a3",foreground="#000000")


# Reddit
reddit = praw.Reddit(client_id='PESO3cS0KquaWQ', client_secret='ALSLenkZwZ5WCZ-32MaziUw-O7tmeA',
                     user_agent='VanillaCast')

red = redditCrawler()
twit = twitterCrawler()
de = dataExport()

dayArray, commentArray, upvotesArray, retweetsArray, likesArray = [], [], [], [], []
# upvotesArray = []
# dayArray = []
# retweetsArray = []
# likesArray = []

# self.graphCanvas
#Initialise plots
#fig, ax = plt.subplots()
#dayArray, commentsArray, upvotesArray, retweetsArray, likesArray
def plotGraph(self, dayArray, commentsArray, upvotesArray, retweetsArray, likesArray):

    plt = self.figure.add_subplot(1, 1, 1)
    x = dayArray

    # now there's 3 sets of points
    yCO = commentsArray
    yUV = upvotesArray
    yRT = retweetsArray
    yLK = likesArray

    plt.plot(x, yCO, label='Comments', marker='o', color='red')
    plt.plot(x, yUV, label='Upvotes', marker='o', color='#fa93b0')
    plt.plot(x, yRT, label='Retweets', marker='o', color='#2374f7')
    plt.plot(x, yLK, label='Likes', marker='o', color='#accafa')

    self.figure.canvas.draw()

def displayDay(self):
    date = self.cBoxGraph.get()
    self.gphLabel.configure(text="Displaying posts from " + str(date))
    if(self.cBoxGraph.get()!=''):
        print("Selected the right date!")
        #Display the day's posts and tweets

def show_entry_fields(self):
    strInput = self.txtSearch.get()
    redResult = ''
    twitResult = ''

    if len(strInput) == 0:
        self.sysLabel.configure(text='Field is empty! Please enter a search term.')
    else:
        self.sysLabel.configure(text='')
        self.lblComments.configure(text='')
        self.lblUpvotes.configure(text='')
        self.lblRetweets.configure(text='')
        self.lblLikes.configure(text='')

        err = ''
        try:
            self.txtReddit.configure(state='normal')
            self.txtTwitter.configure(state='normal')
            redResult = redditCrawl(self, strInput)
            twitResult = twitterCrawl(self, strInput)
            plotGraph(self, dayArray, commentArray, upvotesArray, retweetsArray, likesArray)
            self.txtReddit.configure(state='disabled')
            self.txtTwitter.configure(state='disabled')
            saveQuery(self, strInput)
        except Exception as e:
            err = e
            print('Exception at show_entry_fields: ' + str(e))

        if (err == ''):
            try:
                de.exportData(redResult, strInput)
                de.exportData(twitResult, strInput)
            except Exception as e:
                print('Exception at exporting data: ' + str(e))

def twitterCrawl(self, strInput):
    strVal = self.txtTwitter.get("1.0", 'end')
    if (strVal.strip()):
        self.txtTwitter.delete("1.0", 'end')

    strInput = self.txtSearch.get()
    twitResult = twit.search(strInput)
    twitterCCount = 0
    twitterICount = 0


    for myTwitData in twitResult:
        retweetsArray.append(myTwitData.commentCount)
        likesArray.append(myTwitData.interactionCount)
        twitterCCount += myTwitData.commentCount  # RETWEETS
        twitterICount += myTwitData.interactionCount  # LIKES
        for tweet in myTwitData.getTopComments():
            if 'twitter' in tweet.url.lower():
                self.txtTwitter.insert(tk.END, "\nTweet: \n" + tweet.text)
                self.txtTwitter.insert(tk.END, "\n\nRead More: " + tweet.url)
                self.txtTwitter.insert(tk.END, "\n\nPosted On: " + str(tweet.date))
                self.txtTwitter.insert(tk.END, "\n--------------------------------------------------")
    self.lblRetweets.configure(text="Retweets: " + str(twitterCCount))
    self.lblLikes.configure(text="Likes: " + str(twitterICount))
    print(retweetsArray)
    print(likesArray)
    return twitResult

def redditCrawl(self, strInput):
    str3Val = self.txtReddit.get("1.0", 'end')
    if (str3Val.strip()):
        self.txtReddit.delete("1.0", 'end')
    redResult = red.search(strInput)
    redditCCount = 0
    redditICount = 0


    minDate = ''
    for myRedData in redResult:
        commentArray.append(myRedData.commentCount)
        upvotesArray.append(myRedData.interactionCount)
        redditCCount += myRedData.commentCount  # COMMENTS
        redditICount += myRedData.interactionCount  # UPVOTES
        dayArray.append(myRedData.date)
        for post in myRedData.getTopComments():
            if myRedData.source == "reddit":
                self.txtReddit.insert(tk.END, "\nPost: \n" + post.text)
                self.txtReddit.insert(tk.END, "\n\nRead More: " + post.url)
                self.txtReddit.insert(tk.END, "\n\nPosted On: " + str(datetime.fromtimestamp(post.date)))
                self.txtReddit.insert(tk.END, "\n--------------------------------------------------")
    self.lblComments.configure(text="Comments: " + str(redditCCount))
    self.lblUpvotes.configure(text="Upvotes: " + str(redditICount))
    self.cBoxGraph.config(values=dayArray)
    print(commentArray)
    print(upvotesArray)
    print(dayArray)
    self.gphLabel.configure(text="Displaying posts from " + str(min(dayArray)) + " to " + str(max(dayArray)))

    return redResult

def showSearchHistory(self):
    field = self.txtSearchHistory
    hist = de.getSearchHist()

    strVal = field.get("1.0", 'end')
    if (strVal.strip()): field.delete("1.0", 'end')

    if hist:
        for items in hist:
            field.insert(tk.END, items + "\n")
    field.config(state='disabled')


def saveQuery(self, query):
    items_temp = []
    field = self.txtSearchHistory  # Initialise Search History textbox as 'field'
    field.config(state='normal')  # Enable 'field' for editing (removing and adding texts)
    index = 1

    # Iterate through 'field' to check if query made matches previous searches
    for item in field.get("1.0", 'end').splitlines():
        if item:
            if str(item).lower() == query.lower():
                field.delete(str(index) + '.0',
                             str(index) + '.end + 1 char')  # Remove text from 'field' if matches with current query
        index += 1

    self.txtSearchHistory.insert('1.0', query.capitalize() + "\n")  # Insert current query to first line of 'field'
    field.config(state='disabled')  # Disable user from changing 'field' text box

    # Get updated search history to store in file
    for item in field.get("1.0", 'end').splitlines():
        if item: items_temp.append(item)

    # Store queries (past and current) to file
    de.addSearchHist(items_temp)

if __name__ == '__main__':
    vp_start_gui()
