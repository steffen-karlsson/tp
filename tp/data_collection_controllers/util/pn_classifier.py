#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk import FreqDist, NaiveBayesClassifier, wordpunct_tokenize
from codecs import decode, encode
from random import shuffle
from nltk.corpus import stopwords
from string import punctuation


class MultiTopicClassifier():
    def __init__(self):
        self._da_stopwords = stopwords.words('danish')
        self._topic_sentence_lists = []
        self._all_words_lists = []
        self._classifiers = []

    def train(self, topic_train_files):
        for filename in topic_train_files:
            _word_lists, _all_words = self._tokenize_training_data(filename)
            self._all_words_lists.append(_all_words)
            self._topic_sentence_lists.append(_word_lists)
        for index, all_words in enumerate(self._all_words_lists):
            classifier = self._get_classifier(all_words,
                                              index)
            #classifier.show_most_informative_features(10)
            self._classifiers.append(classifier)
        return self

    def _tokenize_training_data(self, filename):
        words = []
        with open(filename, 'r') as training_file:
            for _line in training_file.readlines():
                word_list = []
                for word in wordpunct_tokenize(decode(_line.split('\t')[0], 'utf-8')):
                    word = encode(word, 'utf-8').translate(None, punctuation)
                    if word:
                        word_list.append(word)
                words.append(word_list)
        return words, [word for word_list in words for word in word_list
                       if word.isalpha() and word not in self._da_stopwords]

    def _get_classifier(self, all_words, index):
        all_words = FreqDist([w.lower() for w in all_words]).keys()[:20]
        _topic_sentence_lists = list(self._topic_sentence_lists)
        sentences = [(list(sentence), True) for sentence in _topic_sentence_lists.pop(index)] \
                    + [(list(sentence), False) for sentence in sum(_topic_sentence_lists, [])]
        shuffle(sentences)
        feature_set = [(self._sentence_features(d, all_words), c) for (d, c) in sentences]
        return NaiveBayesClassifier.train(feature_set)

    @staticmethod
    def _sentence_features(sentence, all_words):
        sentence_words = set(sentence)
        features = {}
        for word in all_words:
            features['contains(%s)' % word] = (word in sentence_words)
        return features

    def classify(self, text):
        text = wordpunct_tokenize(text)
        text = [self._sentence_features(text, all_words)
                for all_words in self._all_words_lists]
        for index, classifier in enumerate(self._classifiers):
            yield classifier.classify(text[index])
