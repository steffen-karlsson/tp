#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose.tools import raises
from tp.data_collection_controllers.util.html_parser import GenericHTMLParser, ParseFailError
from pprint import pprint as ppr

def test_extract_data():
    test_data = "<html><body><div>Data from divtag</div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'data_target_name':'divtagdata',
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'divtagdata':'Data from divtag'
                        }                
    assert result == expected_result

def test_extract_specific_attributes_data():
    test_data = "<html><body><div test='From attribute' class='classname'></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'attribute_target_name':'attribute_data',
                            'return_attributes':['class',],
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'attribute_data':'classname'
                        }                
    assert result == expected_result

def test_extract_multiple_attributes_data():
    test_data = "<html><body><div test='From attribute' class='classname' id='identifier'></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'attribute_target_name':'attribute_data',
                            'return_attributes':['class','id'],
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'attribute_data': ['classname', 'identifier']
                        }                
    assert result == expected_result    

def test_extract_all_attributes_single_attribute():
    test_data = "<html><body><div test='From attribute'></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'attribute_target_name':'attribute_data',
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'attribute_data':('test','From attribute'),
                        }                
    assert result == expected_result

def test_extract_all_attributes_more_than_one_attribute():
    test_data = "<html><body><div test='From attribute' class='classname'></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'attribute_target_name':'attribute_data',
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'attribute_data':
                            [
                                ('test','From attribute'),
                                ('class','classname')
                            ]
                        }                
    assert result == expected_result

@raises(ParseFailError)
def test_extract_non_existant_attribute_data():
    test_data = "<html><body><div test='From attribute' class='classname'></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'attribute_target_name':'attribute_data',
                            'return_attributes':['non-existant-attribute','non-existant-attribute2'],
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)

def test_extract_subtag_data():
    test_data = "<html><body><div><span>Test data</span></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'tag_target_name':'testdata',
                            'subtags':
                            [{
                                'tag':'span',
                                'data_target_name':'subtag_data',
                                'tag_target_name':'testdata',
                            }]
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'subtag_data':'Test data'
                        }              
    assert result == expected_result

def test_reset():
    test_data = "<html><body><div><span>Test data</span></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'tag_target_name':'testdata',
                            'subtags':
                            [{
                                'tag':'span',
                                'data_target_name':'subtag_data',
                                'tag_target_name':'testdata',
                            }]
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    parser.reset()
    result2 = parser.parse(test_data)
    expected_result =   {
                            'subtag_data':'Test data'
                        }              
    assert result == result2
    assert result == expected_result

def test_keep_br_tags():
    test_data = "<html><body><div>Data from divtag<br/></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'data_target_name':'divtagdata',
                            'tag_target_name':'testdata',
                            'keep_break_tags':True,
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'divtagdata':'Data from divtag<br>'
                        }                
    assert result == expected_result

def test_hex_charref():
    test_data = "<html><body><div>Data from divtag&#xE6;&#xF8;&#xE5;</div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'data_target_name':'divtagdata',
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'divtagdata':u'Data from divtagæøå'
                        }                
    assert result == expected_result

def test_decimal_charref():
    test_data = "<html><body><div>Data from divtag&#230;&#248;&#229;</div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'data_target_name':'divtagdata',
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'divtagdata':u'Data from divtagæøå'
                        }                
    assert result == expected_result

def test_ignore():
    test_data = "<html><body><div><span>Test data</span></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'tag_target_name':'testdata',
                            'ignore':True,
                            'subtags':
                            [{
                                'tag':'span',
                                'data_target_name':'subtag_data',
                                'tag_target_name':'testdata',
                            }]
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'subtag_data':'Test data'
                        }              
    assert result == expected_result


def test_ignore_and_multiple_tags():
    test_data = "<html><body><div><span>Test data1</span></div><div><span>Test data2</span></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'tag_target_name':'testdata',
                            'ignore':True,
                            'multiple_tags':True,
                            'subtags':
                            [{
                                'tag':'span',
                                'data_target_name':'subtag_data',
                                'tag_target_name':'testdata',
                            }]
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'subtag_data':['Test data1', 'Test data2']
                        }              
    assert result == expected_result

def test_same_type_of_tag():
    test_data = "<html><body><div test='attribute'>Data from divtag<br/><div></div></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'attributes':('test', 'attribute'),
                            'data_target_name':'divtagdata',
                            'tag_target_name':'testdata',
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'divtagdata':'Data from divtag'
                        }                
    assert result == expected_result

def test_multiple_tags_single_sub_value():
    test_data = "<html><body><div><span>Test data1</span></div><div><span>Test data2</span></div></body></html>"
    parsing_pattern =   [{
                            'tag':'div',
                            'tag_target_name':'testdata',
                            'multiple_tags':True,
                            'subtags':
                            [{
                                'tag':'span',
                                'data_target_name':'subtag_data',
                                'tag_target_name':'subtag_target_name',
                            }]
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'subtag_data':['Test data1', 'Test data2']
                        }              
    assert result == expected_result

def test_multiple_sub_levels():
    test_data = "<html><body><div><span>Test data</span></div></body></html>"
    parsing_pattern =   [{
                            'tag':'body',
                            'tag_target_name':'testdata',
                            'subtags':
                                [{
                                    'tag':'div',
                                    'tag_target_name':'subdiv',
                                    'subtags':
                                        [{
                                            'tag':'span',
                                            'data_target_name':'span_data',
                                        }]
                                }]
                        }]
    parser = GenericHTMLParser(parsing_pattern)
    result = parser.parse(test_data)
    expected_result =   {
                            'span_data':'Test data'
                        }              
    assert result == expected_result