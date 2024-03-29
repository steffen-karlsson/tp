#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: data_processor

"""

from string import digits
from codecs import open
from re import split as resplit
from re import sub as resub
from collections import defaultdict
from os import path
from tp.data_collection_controllers.util.pn_classifier \
    import MultiTopicClassifier


PATTERN = "<br>|\.[^a-zA-Z<]|\n|!|\?"

TITLE_WEIGHT = 0.3
SENTENCE_WEIGHT = 0.7

RMA_PATH = 'tp/data_collection_controllers/util/trainingset_rma.txt'
DELIVERY_PATH = 'tp/data_collection_controllers/util/trainingset_levering.txt'
PRICE_PATH = 'tp/data_collection_controllers/util/trainingset_pris.txt'
if path.isfile(RMA_PATH)\
        and path.isfile(DELIVERY_PATH)\
        and path.isfile(PRICE_PATH):
    CLASSIFIER = MultiTopicClassifier().train([RMA_PATH,
                                               DELIVERY_PATH,
                                               PRICE_PATH])

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
AFINN_PATH = 'tp/data_collection_controllers/util/afinn.txt'
if path.isfile(AFINN_PATH):
    AFINN = {k: int(v.strip()) for k, v in
             [line.split('\t') for line
              in open(AFINN_PATH, 'r', 'utf-8').readlines()
              if not line.startswith('#')]}


def __word_process(word):
    """

    :param word: word to be processed
    :type word: str
    :returns: string -- striped, lower-cased and digits removed word.
    """
    # Removing digits and lower-casing
    return resub(digits, "", word) \
        .strip() \
        .lower()


def __pn_sentiment_score(sentence):
    """

    Calculating sentiment score for a sentence using danish version of
    AFINN (http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010),
    to detect if each word of the sentence is positively or negatively charged
    and accumulate all scores.

    :param sentence: the sentence which needs to be ranked
    :type sentence: str
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

    if total_score > 5:
        total_score = 5
    elif total_score < -5:
        total_score = -5
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
    review.content = review.content.strip()
    review.title = review.title.strip()
    sentences = resplit(PATTERN, review.content)
    topic_score_dict = defaultdict(float)
    for sentence in sentences:
        # for each sentence which is not empty, calculate
        # the pn sentiment score and get the topic(s).
        if sentence:
            topic_score_dict['total_sentence_count'] += 1
            score = __pn_sentiment_score(sentence)
            topics = CLASSIFIER.classify(sentence)
            topic_score_dict["general_score"] += score
            for index, in_topic in enumerate(topics):
                if in_topic:
                    # each sentence can have multiple topics
                    topic = 'rma' if index == 0\
                        else 'delivery' if index == 1\
                        else 'price'
                    topic_score_dict["{}_score".format(topic)] += score
                    topic_score_dict["{}_sentence_count".format(topic)] += 1
    topic_score_dict['title'] = __pn_sentiment_score(review.title)
    title_topics = []
    for index, in_topic in enumerate(list(CLASSIFIER.classify(review.title))):
        if in_topic:
            topic = 'rma' if index == 0\
                else 'delivery' if index == 1\
                else 'price'
            title_topics.append(topic)
    topic_score_dict['title_topics'] = title_topics
    review_scores = defaultdict(float)
    for topic in [_topic for _topic in topic_score_dict.keys()
                  if "_score" in _topic]:
        topic_sentence_score = topic_score_dict[topic]
        topic = topic.split('_')[0]
        if topic == 'general':
            topic_score = topic_sentence_score / \
                topic_score_dict['total_sentence_count']
            if topic_score > 5:
                topic_score = 5
            elif topic_score < -5:
                topic_score = -5
        else:
            sentence_count = topic_score_dict["{}_sentence_count".format(topic)]
            if topic in topic_score_dict.get('title_topics', []):
                topic_score = ((SENTENCE_WEIGHT * topic_sentence_score) +
                               (TITLE_WEIGHT * topic_score_dict['title'])) / \
                              sentence_count
            else:
                topic_score = (SENTENCE_WEIGHT * topic_sentence_score)  / \
                              sentence_count
        # convert from -5/5 to 0-100 due to the progress bars.
        topic_score = (topic_score + 5) * 10
        # boosting score depending on number of stars
        topic_score = topic_score * (0.125*float(review.rating)+0.625)
        if topic_score > 100:
            topic_score = 100
        review_scores[topic] = topic_score
    return review_scores


def ratings_for_company(reviews):
    """

    Calculating sentiment score for all reviews in a company,
    and return a dict containing the values.

    :param reviews: list of reviews for a company
    :type reviews: list
    :returns: dict -- topic as key and score as value
    """

    scores = defaultdict(list)
    for review in reviews:
        for key, value in __review_topic_and_score(review).items():
            scores[key].append(value)
    return scores
