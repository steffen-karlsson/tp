#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
from string import punctuation, digits

da_stopwords = set(stopwords.words('danish'))

# Converting AFINN wordlist to dictionary with word as key
# and happiness score as value
afinn = {k: int(v.strip()) for k, v in
         [line.split('\t') for line
          in open('afinn.txt', 'r').readlines()]}


def __trim_review(review):
    content = review.content
    content_word_list = []
    for word in content.split():
        # If word is not none and not in stopwords add
        if word and word not in da_stopwords:
            content_word_list.append(word)
    # Joining word to string again
    review.content = " ".join(content_word_list)

    title = review.title
    title_word_list = []
    for word in title.split():
        # If word is not none and not in stopwords add
        if word and word not in da_stopwords:
            title_word_list.append(word)
    # Joining word to string again
    review.title = " ".join(title_word_list)
    return review


def __word_process(word):
    # Removing punctuation, digits and lower-casing
    return word.translate(None, punctuation)\
        .translate(None, digits)\
        .strip()\
        .lower()


def __pn_sentiment_score(sentence):
    # Returning the total sum of the sentence based on AFINN scores.
    return sum([afinn.get(word, 0) for word in sentence])


def review_topic_and_score(review):
    review = __trim_review(review)
    #todo: split the review up to multiple sentences if contains multiple topics
    topic = "TBD"
    #todo use classifier to find topic
    score = __pn_sentiment_score(review)
    #todo: rate the score depending on trustpilot score,
    # and a weight of each topic (maybe amount of words for each topic?)
    return topic, score
