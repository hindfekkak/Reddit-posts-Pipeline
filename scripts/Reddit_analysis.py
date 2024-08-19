from datetime import datetime as dt
import pandas as pd
from textblob import TextBlob
import praw

reddit = praw.Reddit(
    client_id='wr8elRs9hX-OCU6Ety7KFQ',
    client_secret='kCjZ8-9QbDbeh9eGrLCBcQuEgB_Bng',
    username='hindfekkak',
    password='Hind@2002',
    user_agent='projet-Pipeline/0.1 by u/hindfekkak'
)

# Example: Fetch top posts from a subreddit
subreddit = reddit.subreddit('chatgpt')

posts = list(subreddit.search("chatgpt", sort='new', time_filter='all', limit=5000))


###################### Post Fact ################################
post_data = []
for post in posts:
    post_dict = {
        "post_id": post.id,
        "post_text": post.selftext.replace("\n", " ")
        .replace("\t", " ")
        .replace(";", " ")
        .replace('"', " "),
        "author_name": post.author.name if post.author else None,
        "comment_count": post.num_comments,
        "upvote_count": post.score,
        "created_at": dt.fromtimestamp(post.created_utc),
        "post_url": post.url,
    }

    post_data.append(post_dict)

post_df = pd.DataFrame(post_data)
post_df.to_csv("reddit_data/post_fact.csv", index=False, sep="|")
print("post_fact done")

############################### Time Dim #############################
time_data = []
for post in posts:
    time_dict = {
        "post_id": post.id,
        "created_at": dt.fromtimestamp(post.created_utc),
        "date": dt.fromtimestamp(post.created_utc).strftime("%Y-%m-%d"),
        "day": dt.fromtimestamp(post.created_utc).day,
        "month": dt.fromtimestamp(post.created_utc).month,
        "year": dt.fromtimestamp(post.created_utc).year,
        "day_of_week": dt.fromtimestamp(post.created_utc).strftime("%A"),
        "time": dt.fromtimestamp(post.created_utc).strftime("%H:%M:%S"),
        "hour": dt.fromtimestamp(post.created_utc).hour,
        "minute": dt.fromtimestamp(post.created_utc).minute,
        "second": dt.fromtimestamp(post.created_utc).second,
    }
    time_data.append(time_dict)

time_df = pd.DataFrame(time_data)
time_df.to_csv("reddit_data/time_dim.csv", index=False, sep="|")
print("time_dim done")

#################### User Dim #################################
user_data = []
for post in posts:
    user_dict = {
        "post_id": post.id,
        "user_name": post.author.name if post.author else None,
    }
    user_data.append(user_dict)

user_df = pd.DataFrame(user_data)
user_df.to_csv("reddit_data/user_dim.csv", index=False, sep="|")
print("user_dim done")

###################################### Sentiment Dim ##################################

def get_sentiment_label(score):
    '''
    A score of +1 very positive sentiment.
    A score between 0.5-1: positive sentiment.
    A score between 0-0.5: a slightly positive sentiment.
    A score of 0: neutral sentiment.
    A score between -0.5-0 : slightly negative sentiment.
    A score between -1_-0.5 :  negative sentiment.
    A score of -1:  very negative sentiment.
    
    Args:
        score (float): sentiment analysis score
    
    Returns:
        tuple: sentiment label and sub-label
    '''
    if score == 1:
        return ("positive", "very positive")
    elif 0.5 <= score < 1:
        return ("positive", "positive")
    elif 0 <= score < 0.5:
        return ("positive", "slightly positive")
    elif score == 0:
        return ("neutral", "neutral")
    elif -0.5 < score < 0:
        return ("negative", "slightly negative")
    elif -1 < score <= -0.5:
        return ("negative", "negative")
    elif score == -1:
        return ("negative", "very negative")


sentiment_data = []
for post in posts:
    # Use TextBlob for sentiment analysis
    blob = TextBlob(post.selftext)
    sentiment = blob.sentiment

    # Calculate score
    score = round(sentiment.polarity, 2)
    sentiment_label = get_sentiment_label(score)
    
    sentiment_dict = {
        "post_id": post.id,
        "post_text": post.selftext.replace("\n", " ")
        .replace("\t", " ")
        .replace(";", " ")
        .replace('"', " "),
        "score": score,
        "general_sentiment": sentiment_label[0],
        "sentiment": sentiment_label[1],
    }

    sentiment_data.append(sentiment_dict)

sentiment_df = pd.DataFrame(sentiment_data)
sentiment_df.to_csv("reddit_data/sentiment_dim.csv", index=False, sep="|")
print("sentiment_dim done")
