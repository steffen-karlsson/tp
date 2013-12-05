#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: data_processor

"""

from string import digits
from re import split as resplit
from collections import defaultdict
from os import path

PATTERN = "<br>|\.[^a-zA-Z<]|\n|!|\?"

TITLE_WEIGHT = 0.3
SENTENCE_WEIGHT = 0.7

NEGATION_WORDS = {'ingen', 'ikke', 'intet', 'aldrig'}
AMPLIFICATION_WORDS = dict({'utrolig': 1.2,
                            'rigtig': 1.2,
                            'absolut': 1.2,
                            'super': 1.2,
                            'mega': 1.2,
                            'virkelig': 1.2,
                            'vildt': 1.2,
                            'dybt': 1.2})

# Converting AFINN wordlist to dictionary with word as key
# and happiness score as value
if path.isfile('afinn.txt'):
    AFINN = {k: int(v.strip()) for k, v in
             [line.split('\t') for line
              in open('afinn.txt', 'r').readlines()
              if not line.startswith('#')]}


def __word_process(word):
    """

    :param word: word to be processed
    :type word: string
    :returns: string -- striped, lower-cased and digits removed word.
    """
    # Removing punctuation, digits and lower-casing
    return word.translate(None, digits) \
        .strip() \
        .lower()


def __pn_sentiment_score(sentence):
    """

    Calculating sentiment score for a sentence using danish version of
    AFINN (http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010),
    to detect if each word of the sentence is positively or negatively charged
    and accumulate all scores.

    :param sentence: the sentence which needs to be ranked
    :type sentence: string
    :returns: float -- sentiment score for the sentence
    """
    # Returning the total sum of the sentence based on AFINN scores.
    negation_factor = 1
    amplification_factor = 1
    total_score = 0
    last_word = ""
    for word in sentence.split():
        word = __word_process(word)
        # Words which is negation or amplification can't affect to the score
        if word in NEGATION_WORDS:
            negation_factor *= -1
        elif word in AMPLIFICATION_WORDS.keys():
            amplification_factor = AMPLIFICATION_WORDS[word]
        else:
            word_score = AFINN.get(word, 0)
            last_word_score = AFINN.get(last_word, 0)
            if word_score == 0 \
                    and amplification_factor > 1\
                    and last_word_score != 0:
                total_score += last_word_score
            else:
                score = word_score \
                        * negation_factor \
                        * amplification_factor
                total_score += score
                amplification_factor = 1
                negation_factor = 1
        last_word = word
    return total_score


def __review_topic_and_score(review):
    """

    Calculating sentiment score for a review, based on all the different
    sentences. Topics within review including body text and title is
    found, and a sentiment score for each of the topics is calculated.

    :param review: the review to determinate differentiated scores
    :type review: Review
    :returns: float -- sentiment score for the sentence
    """
    title = resplit(PATTERN, review.title)
    sentences = resplit(PATTERN, review)
    topic_score_dict = defaultdict(float)
    for sentence in sentences:
        # for each sentense which is not empty, calculate
        # the pn sentiment score and get the topic(s).
        if sentence:
            topic_score_dict['total_sentence_count'] += 1
            score = __pn_sentiment_score(sentence)
            #todo use classifier to find topic
            topics = ["TBD"]
            for topic in topics:
                # each sentence can have multiple topics
                topic_score_dict["{}_score".format(topic)] += score
                topic_score_dict["{}_sentence_count".format(topic)] += 1
    #todo: Title could have more sentences and by that more topics and scores
    topic_score_dict['title'] = __pn_sentiment_score(title)
    topic_score_dict['title_topics'] = ["TBD"]
    review_scores = defaultdict(float)
    for topic in [_topic for _topic in topic_score_dict.keys()
                  if "_score" in _topic]:
        topic_sentence_score = topic_score_dict[topic]
        topic = topic.split('_')[0]
        if topic in topic_score_dict.get('title_topics', []):
            topic_score = ((SENTENCE_WEIGHT * topic_sentence_score) +
                           (TITLE_WEIGHT * topic_score_dict['title'])) *\
                          (topic_score_dict["{}_sentence_count".format(topic)] /
                           topic_score_dict['total_sentence_count'])
        else:
            topic_score = (SENTENCE_WEIGHT * topic_sentence_score) *\
                          (topic_score_dict["{}_sentence_count".format(topic)] /
                           topic_score_dict['total_sentence_count'])
        review_scores[topic] = topic_score
    return review_scores


def get_ratings_for_company(reviews):
    """

    ??

    :param reviews: list of reviews for a company
    :type reviews: list
    :returns: ??
    """
    review_scores = map(__review_topic_and_score, reviews)
    for review_score in review_scores:
        pass
