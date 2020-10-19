import pickle
from pathlib import Path


# TODO - For sprint 1
def load_tweets(city):
    """ Load pickled tweets from file and return tweets as a list """
    city = city.lower()
    city = city.replace("å", "a").replace("ä", "a").replace("ö", "o")
    try:
        with open(f"fallback-tweets/tweets_{city}_1000.p", "rb") as f:
            tweets = pickle.load(f)
            return tweets
    except FileNotFoundError:
        print("Sorry, couldn't find any such file.")
        return []


def calc_mood_score(mood, city):

    # TODO handle keywords
    keywords = {}
    import os
    #print(os.getcwd()) #detta för att se var den plockar keyword? från rätt ställe på burken //CL
    keywords['happy'] = set(Path('keywords/happy_keywords.csv').read_text(encoding='utf8').split(','))
    keywords['angry'] = set(Path('keywords/angry_keywords.csv').read_text(encoding='utf8').split(','))

    tweets = load_tweets(city)

    number_of_tweets = len(tweets)
    if number_of_tweets == 0:
        return -1

    if mood not in keywords:
        print("Mood not available.")

    tweets_with_mood_content = 0
    for tweet in tweets:
        for keyword in keywords.get(mood):
            if keyword in tweet:
                tweets_with_mood_content += 1
                #print(tweet)

    #print(tweets_with_mood_content)

    # TODO implement a better mood score algorithm
    mood_score = (tweets_with_mood_content/number_of_tweets) + 1
    return mood_score
