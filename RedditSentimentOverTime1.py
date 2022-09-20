import praw.models
from nltk.sentiment import SentimentIntensityAnalyzer
import datetime
import matplotlib.pyplot as plt


def Clean(text):
    new_text = ""
    for char in text:
        if char.isalnum() or char == " ":
            new_text += char
    return new_text

user_subreddit = input("Which subreddit would you like to search? ")


reddit_read_only = praw.Reddit(client_id="",
                               client_secret="",
                               user_agent="")

reddit_authorized = praw.Reddit(client_id="",
                                client_secret="",
                                user_agent="",
                                username="",
                                password="")

sia = SentimentIntensityAnalyzer()

TitleList = []
CommentList = []
ReplyList = []

score_list = []
count = 0


for post in reddit_read_only.subreddit(str(user_subreddit)).new(limit=1000):
    if count == 0:
        start_date = datetime.datetime.fromtimestamp(post.created)
    count += 1
    post_time = datetime.datetime.fromtimestamp(post.created)
    print(count)
    print(post_time)
    score_list.append([(-(post_time-start_date).total_seconds()/(60*60*24))])
    score_list[-1].append(sia.polarity_scores(post.title)["compound"])
    TitleList.append((sia.polarity_scores(post.title), post.title))
    TITLE = ("Title: " + post.title + " " + str(sia.polarity_scores(post.title)))
    print(TITLE)
    post.comments.replace_more()
    for comment in post.comments:
        CommentList.append((sia.polarity_scores(comment.body), comment.body))
        score_list[-1].append(sia.polarity_scores(comment.body)["compound"])
        COMMENT = ("   Comment: " + str(comment.body) + " " + str(sia.polarity_scores(comment.body)))
        print(COMMENT)
        for reply in comment.replies:
            ReplyList.append((sia.polarity_scores(reply.body), reply.body))
            score_list[-1].append(sia.polarity_scores(reply.body)["compound"])
            REPLY = ("         Replies: " + str(reply.body) + " " + str(sia.polarity_scores(reply.body)))
            print(REPLY)



print(score_list)

percent_score = []
for post in score_list:
    scores = post[1:]
    negative = 0
    for score in scores:
        if score < 0:
            negative += 1
    if len(scores) > 0:
        neg_perc = negative/len(scores)
        percent_score.append((post[0], neg_perc))

print(percent_score)

plt.title(f"Sentiment of Subreddit {user_subreddit} vs Time")
post_time = [x for x, y in sorted(percent_score, reverse = False)]
negative_ratio = [y for x, y in sorted(percent_score, reverse = False)]
plt.plot(post_time,negative_ratio)

plt.ylabel('% Negative Sentiment')
plt.xlabel(f"Time (Days)  - Start: {start_date}")
plt.legend()
plt.show()

