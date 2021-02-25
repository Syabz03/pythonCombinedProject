import tkinter as tk
import tweepy
import praw

queryLimit = 5

#Twitter
consumer_key = "VpNVndPOykZXjQgfTg2RD21xz"
consumer_secret = "1LyM7m5lTmNWwzUUSJF2kN04B5bZvRStY663PjNEnQRCS6b2QW"
access_token = "1358367734417903620-liyj12fLuUrQGM09nsqiVqiAsFKuRc"
access_token_secret = "r5O5AQYHDZrddrPki5FKDZUritllO3VRSoCIlHJv84UEA"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Creating the authentication object
auth.set_access_token(access_token, access_token_secret) # Setting your access token and secret
api = tweepy.API(auth,wait_on_rate_limit=True) # Creating the API object while passing in auth information

#Reddit
reddit = praw.Reddit(client_id='PESO3cS0KquaWQ', client_secret='ALSLenkZwZ5WCZ-32MaziUw-O7tmeA', user_agent='VanillaCast')

def show_entry_fields():
    strVal = e3.get("1.0",'end')
    if (strVal.strip()):
        e3.delete("1.0",'end')

    val = "Query: %s" % (e1.get())
    e3.insert(tk.END, val)

    query = e1.get() + " -filter:retweets" # The search term you want to find
    language = "en" #language
    results = api.search(q=query, lang=language, rpp=queryLimit) #initiate API call

    for tweet in results: # iterate through every tweets pulled
        # printing the text stored inside the tweet object
        e3.insert(tk.END, "\n\n")
        e3.insert(tk.END, "User: " + tweet.user.screen_name)
        e3.insert(tk.END, "\n")
        e3.insert(tk.END, "Tweeted: \n")
        e3.insert(tk.END, tweet.text)
        e3.insert(tk.END, "\n------------------------------------------------")

    redditCrawl()

def redditCrawl():
    str3Val = e4.get("1.0", 'end')
    if (str3Val.strip()):
        e4.delete("1.0", 'end')

    ml_subreddit = reddit.subreddit(e1.get())

    for post in ml_subreddit.hot(limit=queryLimit):
        e4.insert(tk.END, "\n\n")
        e4.insert(tk.END, "SubReddit: " + str(post.author))
        e4.insert(tk.END, "\n")
        e4.insert(tk.END, "Posted: \n")
        e4.insert(tk.END, post.title)
        e4.insert(tk.END, "\n")
        e4.insert(tk.END, "Description: \n")
        e4.insert(tk.END, post.selftext)
        e4.insert(tk.END, "\n------------------------------------------------")

if __name__ == '__main__':

    window = tk.Tk()
    window.title("Crawler GUI")

    tk.Label(master=window, text="Query").grid(row=0)
    tk.Label(master=window, text="Twitter").grid(row=1, column=0, columnspan=2)
    tk.Label(master=window, text="Reddit").grid(row=1, column=2, columnspan=2)

    e1 = tk.Entry(window)
    e3 = tk.Text(window, width=50, height=30)
    e4 = tk.Text(window, width=50, height=30)

    e1.grid(row=0, column=1)
    e3.grid(row=2, column=0, columnspan=2, sticky=tk.W + tk.E)
    e4.grid(row=2, column=2, columnspan=2, sticky=tk.W + tk.E)

    tk.Button(master=window, text='Show', command=show_entry_fields) \
        .grid(row=0, column=2, sticky=tk.W)
    tk.Button(master=window, text='Quit', command=window.quit) \
        .grid(row=0, column=3, sticky=tk.W)

    tab_parent = tk.Notebook(window)
    tab1 = tk.Frame(tab_parent)
    tab2 = tk.Frame(tab_parent)
    tab_parent.add(tab1, text="All Records")
    tab_parent.add(tab2, text="Add New Record")

    window.mainloop()