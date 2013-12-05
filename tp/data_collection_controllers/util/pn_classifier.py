#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: MultiTopicClassifier

This module only contains the MultiTopicClassifier.
"""

from nltk import FreqDist, NaiveBayesClassifier, wordpunct_tokenize
from codecs import decode, encode
from random import shuffle
from nltk.corpus import stopwords
from string import punctuation


class MultiTopicClassifier(object):
    """
    MultiTopicClassifier is a "container" which contains x number of
    classifiers, the number depends on the number of training sets which
    is used as arguments for the train method.
    """

    def __init__(self):
        """

        This function initializes the MultiTopicClassifier.
        """
        self._da_stopwords = stopwords.words('danish')
        self._topic_sentence_lists = []
        self._all_words_lists = []
        self._classifiers = []

    def train(self, topic_train_files):
        """

        Public function to train x numbers of classifiers depending
        on the number of training sets.

        :param topic_train_files: list of file names for the training sets
        :type topic_train_files: list
        :returns: NaiveBayesClassifier -- trained
        """
        for filename in topic_train_files:
            _word_lists, _all_words = self.__tokenize_training_data(filename)
            self._all_words_lists.append(_all_words)
            self._topic_sentence_lists.append(_word_lists)
        for index, all_words in enumerate(self._all_words_lists):
            classifier = self.__get_classifier(all_words, index)
            #classifier.show_most_informative_features(10)
            self._classifiers.append(classifier)
        return self

    def __tokenize_training_data(self, filename):
        """

        Local function which tokenize a training set from a file name.

        :param filename: file name for the training set
        :type filename: str
        :returns:
        """
        words = []
        with open(filename, 'r') as training_file:
            for _line in training_file.readlines():
                word_list = []
                sentence = decode(_line.split('\t')[0],'utf-8')
                for word in wordpunct_tokenize(sentence):
                    word = encode(word, 'utf-8').translate(None, punctuation)
                    if word:
                        word_list.append(word)
                words.append(word_list)
        return words, [word for word_list in words for word in word_list
                       if word.isalpha() and word not in self._da_stopwords]

    def __get_classifier(self, all_words, index):
        """

        Local function which returns a classifier for a topic,
        depending on the other x-1 topics.

        :param all_words: list of words in a training set
        :type all_words: list
        :param index: index of the current training set
        :type index: int
        :returns: NaiveBayesClassifier -- trained
        """
        all_words = FreqDist([w.lower() for w in all_words]).keys()[:20]
        _topic_sentence_lists = list(self._topic_sentence_lists)
        sentences = [(list(sentence), True) for sentence
                     in _topic_sentence_lists.pop(index)] \
                    + [(list(sentence), False) for sentence
                       in sum(_topic_sentence_lists, [])]
        shuffle(sentences)
        feature_set = [(self.__sentence_features(d, all_words), c)
                       for (d, c) in sentences]
        return NaiveBayesClassifier.train(feature_set)

    @staticmethod
    def __sentence_features(sentence, all_words):
        """

        Local static function which finds the feature set of a sentence from
        the frequency distribution of a training set.

        :param sentence:
        :type sentence: str
        :param all_words:
        :type all_words: FreqDist
        :returns: dict -- feature set
        """
        sentence_words = set(sentence)
        features = {}
        for word in all_words:
            features['contains(%s)' % word] = (word in sentence_words)
        return features

    def classify(self, text):
        """

        Public function which is used to classify text depending on the
        classifiers, which is buid upon the training sets applied using
        the train function. Returns a list of booleans reflecting the
        result of the classifiers.

        :param text: text which needs to be classified
        :type text: str
        :returns: list -- boolean for each classifier.
        """
        text = wordpunct_tokenize(text)
        text = [self.__sentence_features(text, all_words)
                for all_words in self._all_words_lists]
        for index, classifier in enumerate(self._classifiers):
            yield classifier.classify(text[index])
