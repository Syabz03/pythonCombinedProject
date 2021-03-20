import tkinter as tk
import tkinter.ttk as ttk
from crawler import redditCrawler,twitterCrawler
from storage import storage
import sys
import myPage_support
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import copy

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

        top.attributes('-fullscreen', True)
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1, 1)
        top.title("VanillaCast Web Crawler")
        top.configure(background="#f4efe3", highlightbackground="#d9d9d9", highlightcolor="black")

        self.txtSearchHistory = tk.Text(top)
        self.txtSearchHistory.place(relx=0.012, rely=0.278, relheight=0.631, relwidth=0.185)
        self.txtSearchHistory.configure(background="white", foreground="black", font="-family {Segoe UI} -size 15",
                                        highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black",
                                        selectbackground="blue", selectforeground="white", wrap="word")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.012, rely=0.222, height=47, width=332)
        self.Label1.configure(activebackground="#f9f9f9", activeforeground="black", background="#f4efe3",
                              font="-family {Segoe UI Black} -size 15 -weight bold", foreground="#000000",
                              highlightbackground="#d9d9d9", highlightcolor="black", text='''Search History''')

        self.lblReddit = tk.Label(top)
        self.lblReddit.place(relx=0.219, rely=0.222, height=51, width=665)
        self.lblReddit.configure(activebackground="#f9f9f9",activeforeground="black",anchor='n',
                                 background="#F44336",disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI Black} -size 15 -weight bold", foreground="#000000",
                                 highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblReddit.configure(text='''Reddit''')

        self.lblTwitter = tk.Label(top)
        self.lblTwitter.place(relx=0.219, rely=0.352, height=51, width=665)
        self.lblTwitter.configure(activebackground="#f9f9f9",activeforeground="black",anchor='n',
                                  background="#2196F3",disabledforeground="#a3a3a3",
                                  font="-family {Segoe UI Black} -size 15 -weight bold",
                                  foreground="#000000",highlightbackground="#d9d9d9",
                                  highlightcolor="black")
        self.lblTwitter.configure(text='''Twitter''')

        self.lblComments = tk.Label(top)
        self.lblComments.place(relx=0.219, rely=0.259, height=40, width=665)
        self.lblComments.configure(anchor='nw',background="#ffc4c4",disabledforeground="#a3a3a3",foreground="#000000",font="-family {Segoe UI} -size 15")
        self.lblComments.configure(text='''Comments: -''')

        self.lblRetweets = tk.Label(top)
        self.lblRetweets.place(relx=0.219, rely=0.389, height=39, width=665)
        self.lblRetweets.configure(activebackground="#f9f9f9",activeforeground="black",anchor='nw',background="#b9edf4",
                                   disabledforeground="#a3a3a3",foreground="#000000",font="-family {Segoe UI} -size 15",
                                   highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblRetweets.configure(text='''Retweets: -''')

        self.lblUpvotes = tk.Label(top)
        self.lblUpvotes.place(relx=0.219, rely=0.296, height=40, width=665)
        self.lblUpvotes.configure(activebackground="#f9f9f9",activeforeground="black",anchor='nw',
                                  background="#ffc4c4",disabledforeground="#a3a3a3",
                                  font="-family {Segoe UI} -size 15",foreground="#000000",
                                  highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblUpvotes.configure(text='''Upvotes: -''')

        self.lblLikes = tk.Label(top)
        self.lblLikes.place(relx=0.219, rely=0.426, height=40, width=665)
        self.lblLikes.configure(activebackground="#f9f9f9",activeforeground="black",
                                anchor='nw',background="#b9edf4",disabledforeground="#a3a3a3",font="-family {Segoe UI} -size 15",
                                foreground="#000000",highlightbackground="#d9d9d9",highlightcolor="black")
        self.lblLikes.configure(text='''Likes: -''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.28, rely=0.167, height=47, width=460)
        self.Label2.configure(activebackground="#f9f9f9", activeforeground="black", background="#f4efe3",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 15 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Interaction Count for the week''')

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=top)

        self.Label5 = tk.Label(top)
        self.Label5.place(relx=0.339, rely=0.472, height=47, width=205)
        self.Label5.configure(activebackground="#f9f9f9", activeforeground="black", background="#f4efe3",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 15 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Graph''')

        self.txtReddit = tk.Text(top, state='disabled')
        self.txtReddit.place(relx=0.597, rely=0.093, relheight=0.35, relwidth=0.39)
        self.txtReddit.configure(background="white", font="-family {Segoe UI} -size 15", foreground="black",
                                 highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black",
                                 selectbackground="blue", selectforeground="white", wrap="word")

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.597, rely=0.037, height=46, width=749)
        self.Label3.configure(activebackground="#f9f9f9", activeforeground="black", background="#F44336",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 15 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Reddit''')

        self.txtTwitter = tk.Text(top, state='disabled')
        self.txtTwitter.place(relx=0.597, rely=0.519, relheight=0.389, relwidth=0.39)
        self.txtTwitter.configure(background="white", font="-family {Segoe UI} -size 15", foreground="black",
                                  highlightbackground="#2196F3", highlightcolor="black", insertbackground="black",
                                  selectbackground="blue", selectforeground="white", wrap="word")

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.597, rely=0.463, height=47, width=741)
        self.Label4.configure(activebackground="#f9f9f9", activeforeground="black", background="#2196F3",
                              disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 15 -weight bold",
                              foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                              text='''Twitter''')

        self.txtSearch = tk.Entry(top)
        self.txtSearch.place(relx=0.012, rely=0.019, relheight=0.076, relwidth=0.403)
        self.txtSearch.configure(font="-family {Segoe UI Black} -size 15 -weight bold")

        self.btnSearch = tk.Button(top)
        self.btnSearch.place(relx=0.426, rely=0.019, height=44, width=87)
        self.btnSearch.configure(activebackground="#fafeda", activeforeground="#000000", background="#1DE9B6",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 15 -weight bold",
                                 foreground="#000000", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0",
                                 text='''Search''')

        self.btnQuit = tk.Button(top)
        self.btnQuit.place(relx=0.927, rely=0.934, height=44, width=117)
        self.btnQuit.configure(activebackground="#ececec", activeforeground="#000000", background="#FF1744",
                               disabledforeground="#a3a3a3", font="-family {Segoe UI Black} -size 15 -weight bold",
                               foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                               text='''Quit''')

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.btnSearch.configure(command=lambda: show_entry_fields(self))
        self.btnQuit.configure(command=root.quit)

        showSearchHistory(self)

        self.sysLabel = tk.Label(top)
        self.sysLabel.place(relx=0.012, rely=0.111, height=40, width=781)
        self.sysLabel.configure(activebackground="#f9f9f9", activeforeground="black",anchor='w',background="#f4efe3",
                                disabledforeground="#a3a3a3",font="-family {Segoe UI} -size 15 -slant italic",
                                foreground="#eb3034",highlightbackground="#d9d9d9",highlightcolor="black",justify='left')

        self.cBoxGraph = ttk.Combobox(top, state='readonly') #PLACEHOLDER
        self.cBoxGraph.place(relx=0.219, rely=0.926, relheight=0.039, relwidth=0.074)
        self.cBoxGraph.configure(takefocus="")

        self.gphLabel = tk.Label(top)
        self.gphLabel.place(relx=0.305, rely=0.926, height=39, width=825)
        self.gphLabel.configure(anchor='w',background="#f4efe3",disabledforeground="#a3a3a3",foreground="#000000")



red = redditCrawler()
twit = twitterCrawler()
de = storage()

dayArray, commentsArray, upvotesArray, retweetsArray, likesArray = [], [], [], [], []

def plotGraph(self, dayArray, commentsArray, upvotesArray, retweetsArray, likesArray):
    """A function to plot graph using module matplotlib based on the 5 array parameters and its value to display the topic's interaction count for the week

            Args:
                dayArray : arr
                    the array containing the date ranges within the week of crawling
                commentsArray : arr
                    the array containing respective days' number of comments
                upvotesArray : arr
                    the array containing respective days' number of upvotes
                retweetsArray : arr
                    the array containing respective days' number of retweets
                likesArray : arr
                    the array containing respective days' number of likes

    """
    self.canvas.get_tk_widget().place(relx=0.219, rely=0.519, relheight=0.389, relwidth=0.352)

    # Clears graph before plotting to prevent appending two graphs at once
    self.figure.clear()
    # self.figure.
    plt = self.figure.add_subplot(1, 1, 1)
    x = []
    max_log_size = 5000
    for i in dayArray:
        i = ''.join(i.split())
        i = i[:-5]
        x.append(i)
    print(x)

    # now there's 3 sets of points
    yCO = commentsArray
    yUV = upvotesArray
    yRT = retweetsArray
    yLK = likesArray

    if max(yCO)>=max_log_size or max(yUV)>=max_log_size or max(yRT)>=max_log_size or max(yLK)>=max_log_size:
        plt.set(yscale="log")
    plt.plot(x, yCO, label='Comments', marker='o', color='red')
    plt.plot(x, yUV, label='Upvotes', marker='o', color='#fa93b0')
    plt.plot(x, yRT, label='Retweets', marker='o', color='#2374f7')
    plt.plot(x, yLK, label='Likes', marker='o', color='#accafa')

    plt.legend()
    self.figure.canvas.draw()

def show_entry_fields(self):
    """A function to initialise elements in TKinter GUI and main functions for the program

    Attributes:
        redResult : list
            to store list of Mydata objects of posts returned from crawler APIs
        twitResult : list
            to store list of Mydata objects of tweets returned from crawler APIs
        err : str
            to store exception error messages

    """
    strInput = self.txtSearch.get()
    redResult = ''
    twitResult = ''


    if len(dayArray)!=0 or len(commentsArray)!=0 or len(upvotesArray)!=0 or len(retweetsArray)!=0 or len(likesArray)!=0:
        dayArray.clear()
        commentsArray.clear()
        upvotesArray.clear()
        retweetsArray.clear()
        likesArray.clear()

    if len(strInput) == 0 or len(strInput.strip()) == 0:
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
            displayRedditPosts(self, redResult)
            twitResult = twitterCrawl(self, strInput)
            displayTwitterTweets(self, twitResult)
            print("=====Main====")
            for post in redResult:
                for i in post.getTopComments():
                    print(i)

            self.cBoxGraph.bind("<<ComboboxSelected>>", lambda _: displayDay(self, redResult, twitResult))
            plotGraph(self, dayArray, commentsArray, upvotesArray, retweetsArray, likesArray)
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
                pass
            except Exception as e:
                print('Exception at exporting data: ' + str(e))

def displayDay(self, redResult, twitResult):
    """A function to display the posts and tweets based on date

        Args:
            redResult : List
                the list of Mydata object which each contains reddit posts crawled for the respective days of the week
            twitResult : List
                the list of Mydata object which each contains twitter tweets crawled for the respective days of the week

    """
    date = self.cBoxGraph.get()
    date_obj = datetime.strptime(date, '%d-%m-%Y')
    date_obj = date_obj.strftime("%Y-%m-%d")
    date = str(date_obj)

    self.txtReddit.configure(state='normal')
    self.txtTwitter.configure(state='normal')

    if(self.cBoxGraph.get()!=''):
        self.txtReddit.delete("1.0", 'end')
        self.txtTwitter.delete("1.0", 'end')
        #Display the day's posts and tweets
        for myRedData in redResult:
            for post in myRedData.getTopComments():
                if date in str(datetime.fromtimestamp(post.getDate())):
                    self.txtReddit.insert(tk.END, "\nPost: \n" + post.getText())
                    self.txtReddit.insert(tk.END, "\n\nRead More: " + post.getUrl())
                    self.txtReddit.insert(tk.END, "\n\nPosted On: " + str(datetime.fromtimestamp(post.getDate())))
                    self.txtReddit.insert(tk.END, "\n---------------------------------------------------------------------------------------------")
        for myTwit in twitResult:
            for tweet in myTwit.getTopComments():
                if date in str(tweet.getDate()):
                   self.txtTwitter.insert(tk.END, "\nTweet: \n" + tweet.getText())
                   self.txtTwitter.insert(tk.END, "\n\nRead More: " + tweet.getUrl())
                   self.txtTwitter.insert(tk.END, "\n\nPosted On: " + str((tweet.getDate())))
                   self.txtTwitter.insert(tk.END, "\n---------------------------------------------------------------------------------------------")
        if self.txtTwitter.compare("end-1c", "==", "1.0"):
            self.txtTwitter.insert(tk.END, "No tweets found on this day!")
        if self.txtReddit.compare("end-1c", "==", "1.0"):
            self.txtReddit.insert(tk.END, "No posts found on this day!")

    self.gphLabel.configure(text="Displaying results from " + str(date))
    self.txtReddit.configure(state='disabled')
    self.txtTwitter.configure(state='disabled')

def twitterCrawl(self, strInput):
    """A function to call twitter crawler search function to return the list of Mydata objects

    Args:
        strInput : str
            the topic or input searched by the user.

    Attributes:
        strVal : str
            obtain the field on the UI that contains all twitter tweets

    """
    strVal = self.txtTwitter.get("1.0", 'end')
    if (strVal.strip()):
        self.txtTwitter.delete("1.0", 'end')
    twitResult = twit.search(strInput)
    print("====Twitter====")
    for post in twitResult:
        for i in post.getTopComments():
            print(i)

    return twitResult

def displayTwitterTweets(self, twitResult):
    """A function to display Twitter tweets and interaction counts on the TKinter elements

    Args:
        twitResult : List
            the list of Mydata object which each contains twitter tweets crawled for the respective days of the week

    Attributes:
        twitterCCount : int
            to keep count of number of tweets for all tweets displayed for the week
        twitterICount : int
            to keep count of number of likes for all tweets displayed for the week

    """
    strVal = self.txtTwitter.get("1.0", 'end')
    if (strVal.strip()):
        self.txtTwitter.delete("1.0", 'end')
    twitterCCount = 0
    twitterICount = 0

    for myTwitData in twitResult:
        retweetsArray.append(myTwitData.commentCount)
        likesArray.append(myTwitData.interactionCount)
        twitterCCount += myTwitData.commentCount  # RETWEETS
        twitterICount += myTwitData.interactionCount  # LIKES
        self.txtTwitter.insert(tk.END, "\n=====================================================")
        for tweet in myTwitData.getTopComments():
            if 'twitter' in tweet.url.lower():
                self.txtTwitter.insert(tk.END, "\nTweet: \n" + tweet.getText())
                self.txtTwitter.insert(tk.END, "\n\nRead More: " + tweet.getUrl())
                self.txtTwitter.insert(tk.END, "\n\nPosted On: " + str(tweet.getDate()))
                self.txtTwitter.insert(tk.END, "\n---------------------------------------------------------------------------------------------")
    self.lblRetweets.configure(text="Retweets: " + str(twitterCCount))
    self.lblLikes.configure(text="Likes: " + str(twitterICount))

def redditCrawl(self, strInput):
    """A function to call reddit crawler search function to return the list of Mydata objects

    Args:
        strInput : str
            the topic or input searched by the user.

    Attributes:
        str3Val : str
            obtain the field on the UI that contains all reddit posts

    """
    str3Val = self.txtReddit.get("1.0", 'end')
    if (str3Val.strip()):
        self.txtReddit.delete("1.0", 'end')
    redResult = red.search(strInput)
    return redResult

def displayRedditPosts(self, redResult):
    """A function to display Reddit posts and interaction counts on the TKinter elements

    Args:
        redResult : List
            the list of Mydata object which each contains reddit posts crawled for the respective days of the week

    Attributes:
        redditCCount : int
            to keep count of number of comments for all posts displayed
        redditICount : int
            to keep count of number of upvotes for all posts displayed
        dayArray : arr
            to keep track of the list of dates returned in redResult to be used for combobox values loading

    """
    str3Val = self.txtReddit.get("1.0", 'end')
    if (str3Val.strip()):
        self.txtReddit.delete("1.0", 'end')
    redditCCount = 0
    redditICount = 0

    for myRedData in redResult:
        commentsArray.append(myRedData.commentCount)
        upvotesArray.append(myRedData.interactionCount)
        redditCCount += myRedData.commentCount  # COMMENTS
        redditICount += myRedData.interactionCount  # UPVOTES
        dayArray.append(myRedData.date)
        self.txtReddit.insert(tk.END, "\n=====================================================")
        for post in myRedData.getTopComments():
            if myRedData.source == "reddit":
                self.txtReddit.insert(tk.END, "\nPost: \n" + post.getText())
                self.txtReddit.insert(tk.END, "\n\nRead More: " + post.getUrl())
                self.txtReddit.insert(tk.END, "\n\nPosted On: " + str(datetime.fromtimestamp(post.getDate())))
                self.txtReddit.insert(tk.END, "\n---------------------------------------------------------------------------------------------")
    self.lblComments.configure(text="Comments: " + str(redditCCount))
    self.lblUpvotes.configure(text="Upvotes: " + str(redditICount))

    #Populate combobox with values consisting of dates from the posts.
    self.cBoxGraph.config(values=dayArray)
    self.gphLabel.configure(text="Displaying posts from " + str(min(dayArray)) + " to " + str(max(dayArray)))

def showSearchHistory(self):
    """A function to display previous user searches to UI

    Attributes:
        field : Tkinter's Text()
            obtains the text in the field on the UI that contains all previous searches
        hist : list
            contains user's previous searches

    """
    field = self.txtSearchHistory
    hist = de.getSearchHist()

    strVal = field.get("1.0", 'end')
    if (strVal.strip()): field.delete("1.0", 'end')

    if hist:
        for items in hist:
            field.insert(tk.END, items + "\n")
    field.config(state='disabled')

def saveQuery(self, query):
    """A function to add new user's search to file

    Args:
        query : str
            the topic or input searched by the user.

    Attributes:
        items_temp : arr
            temp array to store all previous and current searches before writing to file
        field : txtBox
            obtain the field on the UI that contains all previous searches
        index : int
            to keep count of current for loop's iteration count

    """
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
