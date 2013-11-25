#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk import FreqDist, NaiveBayesClassifier
from codecs import decode
from random import shuffle

TRAIN_FILE = 'trainingset.txt'
INX_WORD = 0
INX_TOPIC = 1


def __get_training_data(topic):
    sentence_set = []
    word_list = []
    with open(TRAIN_FILE, 'r') as training_file:
        for _line in training_file.readlines():
            _sentence_topic = _line.split('\t')
            sentence = decode(_sentence_topic[INX_WORD], 'utf-8')
            #If the _topic is the desired topic the word is positive else negative
            _topic = _sentence_topic[INX_TOPIC].rstrip()
            if topic == _topic:
                for word in sentence.split():
                    if word.isalpha():
                        word_list.append(word)
                sentence_set.append((sentence, 'positive'))
            else:
                sentence_set.append((sentence, 'negative'))
    shuffle(sentence_set)
    return sentence_set, word_list


def __get_word_features(word_list):
    word_list = FreqDist(word_list)
    word_features = word_list.keys()
    return word_features


def extract_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def __get_generic_classifier(topic):
    sentence_set, word_list = __get_training_data(topic)
    word_list = FreqDist([w.lower() for w in word_list])
    feature_set = []
    for (sentence, topic) in sentence_set:
        feature_set.append((extract_features(sentence, word_list), topic))
    return NaiveBayesClassifier.train(feature_set)


def get_rma_classifier():
    return __get_generic_classifier('rma')


def get_price_classifier():
    return __get_generic_classifier('price')


def get_delivery_classifier():
    return __get_generic_classifier('levering')
