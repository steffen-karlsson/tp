#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.html_parser import GenericHTMLParser


def _create_category_parser():
    parsing_pattern = [
                        {
                            'tag':'div',
                            'attributes':('class', 'item clearfix'),
                            'multiple_tags':True,
                            'ignore':True,
                            'subtags':
                            [{
                                'tag':'h3',
                                'ignore':True,
                                'subtags':
                                [{
                                    'tag':'a',
                                    'return_attributes':['href'],
                                    'data_target_name':'ranking',
                                    'attribute_target_name':'url',
                                    'tag_target_name':'companies',
                                }]
                            }]
                        }
                      ]
    return GenericHTMLParser(parsing_pattern)


def _create_review_parser():
    parsing_pattern = __create_review_parser_pattern()
    return GenericHTMLParser(parsing_pattern)

def _create_review_parser_first():
    parsing_pattern = __create_review_parser_pattern()
    parsing_pattern.extend([{
                            'tag':'meta',
                            'attributes':('itemprop', 'reviewCount'),
                            'return_attributes':['content'],
                            'attribute_target_name':'review_count',
                            'tag_target_name':'review_count',
                        },
                        {
                            'tag':'span',
                            'attributes':('itemprop', 'ratingValue'),
                            'data_target_name':'tp_score',
                        }])
    return GenericHTMLParser(parsing_pattern)


def __create_review_parser_pattern():
    parsing_pattern = [
                        {
                            'tag':'div',
                            'attributes':('itemprop', 'review'),
                            'multiple_tags':True,
                            'return_attributes':['data-reviewid'],
                            'attribute_target_name':'tp_review_id',
                            'tag_target_name':'reviews',
                            'subtags':
                            [{
                                'tag':'div',
                                'attributes':('class', 'profileinfo'),
                                'tag_target_name':'user',
                                'subtags':
                                [{
                                    'tag':'a',
                                    'attributes':('itemprop', 'author'),
                                    'data_target_name':'author',
                                    'tag_target_name':'author',
                                },
                                {
                                    'tag':'span',
                                    'attributes':('class', 'reviewsCount'),
                                    'data_target_name':'review_count',
                                    'tag_target_name':'review_count',
                                }]
                            },
                            {
                                'tag':'meta',
                                'attributes':('itemprop', 'ratingValue'),
                                'return_attributes':['content'],
                                'attribute_target_name':'rating',
                            },
                            {
                                'tag':'time',
                                'return_attributes':['datetime'],
                                'attribute_target_name':'created_at',
                            },
                            {
                                'tag':'a',
                                'attributes':('class', 'showReview'),
                                'data_target_name':'title',
                            },
                            {
                                'tag':'p',
                                'attributes':('itemprop', 'reviewBody'),
                                'data_target_name':'content',
                                'keep_break_tags':True,
                            }]
                        }
                      ]
    return parsing_pattern