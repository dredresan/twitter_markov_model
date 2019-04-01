#!/usr/bin/env python
# encoding: utf-8

import re
import tweepy 
import markovify
import pandas as pd
import json
import spacy

# Your Twitter credentials go here (See https://developer.twitter.com/en/docs/basics/authentication/overview to get them)
api_key = ""
api_secret = ""
access_token = ""
access_secret = ""

# Set the tweet handle/screen name that you want to download from 
tweet_handle = ""

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

all_the_tweets = []
tweets = api.user_timeline(screen_name = tweet_handle, count=200, tweet_mode='extended', include_rts=False)
all_the_tweets.extend(tweets)
oldest = all_the_tweets[-1].id - 1

while len(tweets) > 0:
    tweets = api.user_timeline(screen_name = tweet_handle, count=200, max_id=oldest, tweet_mode='extended', include_rts=False)
    all_the_tweets.extend(tweets)
    oldest = all_the_tweets[-1].id - 1
    print ("Number of tweets downloaded so far" % (len(all_the_tweets)))

training_text = " ".join(all_the_tweets)

# Clean tweets by taking out mentions, links, and hashtags.  
cleaned_text = re.sub(r"[@#][\w_-]+", "", training_text, flags=re.MULTILINE)
cleaned_text = re.sub(r'https?://\S+', '', cleaned_text, flags=re.MULTILINE)
cleaned_text = re.sub(r'amp;', '', cleaned_text, flags=re.MULTILINE)

# Use spaCy to extend the Markovify Text class so that we can use parts-of-speech to help with model creation 
nlp = spacy.load("en")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

# Train Markov Model with text (this can take a few minutes)
model = POSifiedText(text, state_size=3)

# Prints Markov generated text to console
for i in range(5):
    print(model.make_short_sentence(140))

# Prints Markov generated text to console using a sentence seed (e.g., "I")
for i in range(5):
    print(model.make_sentence_with_start("I", strict=False))



