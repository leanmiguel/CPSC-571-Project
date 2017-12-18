from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib

# twitter credentials, developer api code    

 
consumer_key = 'OlQzyhMG8KbVidEvtS26xnVlc'
consumer_secret = 'fTR509g6Exc5Eq4TEhv16OeEsTz1S1LY8r29A98BJtZdoXRKEq'
access_token = '925367333840871427-E3y9myxlSzCutQfAaUBCYCBEk0WFxP7' 
access_token_secret = 'pXOK4wv3gkkbl3TBfKhkP7xZQS8vJOd1gM8rX6oLwfChi'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#initialize vader, sentiment analyser library
analyser = SentimentIntensityAnalyzer()


tweetList = []
userNameList = []
userTweetList = []
sentimentRatingList = []
dateList = []
classifiedSentimentList = [0,0,0]
query = ""
max_tweets = 100
LARGE_FONT = ("Verdana", 12)


def main(): 
    #get access to twitter api thru tweepy library
    global tweetList, userNameList, userTweetList, sentimentRatingList, classifiedSentimentList, dateList, query
    
    #if there is no query in the box, do nothing
    if (query == ""):
        return
    #reset all lists for next query
    tweetList = []
    userNameList = []
    userTweetList= []
    dateList = []
    sentimentRatingList = []
    classifiedSentimentList = [0,0,0]
    tweetList = retrieveTweets()
    gatherTweetList(tweetList) 


    # remove unneccesary text in tweet
def cleanTweet(string):    
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",string).split())
    return text
    
def retrieveTweets():               
    
    return ([status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)])
    
# create lists needed to generate graphs and csv
def gatherTweetList(list):

    for tweet in list:
        userNameList.append(tweet.user.screen_name)
        userTweetList.append(cleanTweet(tweet.text))
        sentimentRatingList.append(analyser.polarity_scores(cleanTweet(tweet.text))['compound'])
        dateList.append(tweet.created_at)

        if (analyser.polarity_scores(cleanTweet(tweet.text))['compound'] > 0 ) :
            classifiedSentimentList[0] += 1
        elif (analyser.polarity_scores(cleanTweet(tweet.text))['compound'] == 0) :
            classifiedSentimentList[2] += 1
        else :
            classifiedSentimentList[1] += 1

def createCSV():

    if (query == ""):
        return
    
    with open('twitterSentimentAnalysisFile.csv', "w", encoding="utf-8", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')  
            writer.writerow(['username', 'tweet', 'sentiment rating','date posted'])
            for i in range(0,len(userNameList)):
                writer.writerow([userNameList[i], userTweetList[i], str(sentimentRatingList[i]), dateList[i]])
      
def createSentimentGraph():

      if (query == ""):
          return
      objects = ('POS','NEG','NEU')
      vals = (classifiedSentimentList[0],classifiedSentimentList[1],classifiedSentimentList[2])
      y_pos = np.arange(len(vals))
      posVals = classifiedSentimentList[0]
      negVals = classifiedSentimentList[1]
      neuVals = classifiedSentimentList[2]          
      plt.bar(0, posVals, label = 'positive', color = 'green')
      plt.bar(1, negVals, label= 'neg', color = 'red')
      plt.bar(2, neuVals, label= 'positive', color = 'gray')
      plt.xticks(y_pos, objects)
      plt.xlabel('Sentiment')
      plt.ylabel('Number of Tweets')
      plt.title('Sentiment Value Graph for query \'' + query + '\'')
      plt.show()

class GraphicalUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="twitterico.ico")
        tk.Tk.wm_title(self, "Twitter Sentiment Analysis Tool")
       
        # container is the window that everythingg is contained in.
        container = tk.Frame(self)
        container.pack(side="top", expand = True)
        
        #frames are the individual pages that are displayed, startpage, pageone 

        self.frames = {}

        for F in (StartPage,PageOne,PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column= 0, sticky ="nsew")
            

        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.master.tk_setPalette(background = '#4286f4')
        label = tk.Label(self, text="Twitter Sentiment Analyser", font=("Verdana", 50)).pack(padx=10,expand =True)

        tk.Label(self, text = "Sentiment analysis is the classification of whether a given text input is positive, negative or neutral." , font = ("Verdana", 15)).pack(padx = 5)
        tk.Label(self, text = "This program allows a user to input a query and find twitter's recent opinion of the query." , font = ("Verdana", 10)).pack() 
        tk.Label(self, text = "You may also be able to retrieve the CSV file of the query filled with the username,tweets, and associated sentiment value." , font = ("Verdana", 10)).pack() 
        #lambda allows the button press to execute multiples times
        continueButton = ttk.Button(self, text = "Continue", command=lambda:controller.show_frame(PageOne)).pack(pady= (15,5))
        quitButton = ttk.Button(self, text = "Quit", command=quit).pack(pady=10)

 

     

def setQuery(string):
    global query
    query = string

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

class PageOne(tk.Frame):
    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Twitter Sentiment Analyser", font=("Verdana", 50)).pack(pady=10, padx=10)

        tk.Label(self, text = "Query" , font = ("Verdana", 15)).pack()
        queryEntry = tk.Entry(self, width =30, font= ("Verdana", 25))
        queryEntry.pack(pady = 10)
 
        analyzeQueryButton = ttk.Button(self, text = "Analyze query", command=lambda: combine_funcs(setQuery(queryEntry.get()),main(), createSentimentGraph())).pack(pady = 10)
        retrieveCSVButton = ttk.Button(self,text = "Retrieve Tweets from Query in a CSV file", command=lambda:  combine_funcs(setQuery(queryEntry.get()),main(), createCSV())).pack(pady = 10)
        returnButton = ttk.Button(self, text = "Back to Instructions", command=lambda:controller.show_frame(StartPage)).pack(pady = 10)
               

class PageTwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Sentiment Bar Graph", font="LARGE_FONT")
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text = "Back to Home", command=lambda:controller.show_frame(StartPage))
        button1.pack()
 
app = GraphicalUI()
app.mainloop()