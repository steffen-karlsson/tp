#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.html_parser import HTMLParser2


def _create_category_parser():
    parsing_pattern = [
                        {
                            'tag':'div',
                            'attributes':('class', 'item clearfix'),
                            'multiple_tags':True,
                            'returnattributes':None,
                            'ignore':True,
                            'data_target_name':None,
                            'attribute_target_name':None,
                            'tag_target_name':None,
                            'subtags':
                            [{
                                'tag':'h3',
                                'attributes':None,
                                'multiple_tags':False,
                                'returnattributes':None,
                                'ignore':True,
                                'data_target_name':None,
                                'attribute_target_name':None,
                                'tag_target_name':None,
                                'subtags':
                                [{
                                    'tag':'a',
                                    'attributes':None,
                                    'multiple_tags':False,
                                    'returnattributes':['href'],
                                    'ignore':False,
                                    'data_target_name':'ranking',
                                    'attribute_target_name':'url',
                                    'tag_target_name':'companies',
                                    'subtags':None
                                }]
                            }]
                        }
                      ]
    return HTMLParser2(parsing_pattern)


def _create_review_parser():
    parsing_pattern = __create_review_parser_pattern()
    return HTMLParser2(parsing_pattern)

def _create_review_parser_first():
    parsing_pattern = __create_review_parser_pattern()
    parsing_pattern.extend([{
                            'tag':'meta',
                            'attributes':('itemprop', 'reviewCount'),
                            'multiple_tags':False,
                            'returnattributes':['content'],
                            'ignore':False,
                            'data_target_name':None,
                            'attribute_target_name':'review_count',
                            'tag_target_name':'review_count',
                            'subtags':None
                        },
                        {
                            'tag':'span',
                            'attributes':('itemprop', 'ratingValue'),
                            'multiple_tags':False,
                            'returnattributes':None,
                            'ignore':False,
                            'data_target_name':'tp_score',
                            'attribute_target_name':None,
                            'tag_target_name':None,
                            'subtags':None
                        }])
    return HTMLParser2(parsing_pattern)


def __create_review_parser_pattern():
    parsing_pattern = [
                        {
                            'tag':'div',
                            'attributes':('itemprop', 'review'),
                            'multiple_tags':True,
                            'returnattributes':['data-reviewid'],
                            'ignore':False,
                            'data_target_name':None,
                            'attribute_target_name':'tp_review_id',
                            'tag_target_name':'reviews',
                            'subtags':
                            [{
                                'tag':'div',
                                'attributes':('class', 'profileinfo'),
                                'multiple_tags':False,
                                'returnattributes':None,
                                'ignore':False,
                                'data_target_name':None,
                                'attribute_target_name':None,
                                'tag_target_name':'user',
                                'subtags':
                                [{
                                    'tag':'a',
                                    'attributes':('itemprop', 'author'),
                                    'multiple_tags':False,
                                    'returnattributes':None,
                                    'ignore':False,
                                    'data_target_name':'author',
                                    'attribute_target_name':None,
                                    'tag_target_name':'author',
                                    'subtags':None
                                },
                                {
                                    'tag':'span',
                                    'attributes':('class', 'reviewsCount'),
                                    'multiple_tags':False,
                                    'returnattributes':None,
                                    'ignore':False,
                                    'data_target_name':'review_count',
                                    'attribute_target_name':None,
                                    'tag_target_name':'review_count',
                                    'subtags':None
                                }]
                            },
                            {
                                'tag':'meta',
                                'attributes':('itemprop', 'ratingValue'),
                                'multiple_tags':False,
                                'returnattributes':['content'],
                                'ignore':False,
                                'data_target_name':None,
                                'attribute_target_name':'rating',
                                'tag_target_name':None,
                                'subtags': None
                            },
                            {
                                'tag':'time',
                                'attributes':None,
                                'multiple_tags':False,
                                'returnattributes':['datetime'],
                                'ignore':False,
                                'data_target_name':None,
                                'attribute_target_name':'created_at',
                                'tag_target_name':None,
                                'subtags': None
                            },
                            {
                                'tag':'a',
                                'attributes':('class', 'showReview'),
                                'multiple_tags':False,
                                'returnattributes':None,
                                'ignore':False,
                                'data_target_name':'title',
                                'attribute_target_name':None,
                                'tag_target_name':None,
                                'subtags': None
                            },
                            {
                                'tag':'p',
                                'attributes':('itemprop', 'reviewBody'),
                                'multiple_tags':False,
                                'returnattributes':None,
                                'ignore':False,
                                'data_target_name':'content',
                                'attribute_target_name':None,
                                'tag_target_name':None,
                                'subtags': None
                            }]
                        }
                      ]
    return parsing_pattern