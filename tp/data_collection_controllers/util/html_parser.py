#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: GenericHTMLParser

"Generic" SAX-styled event driven HTML parser
Idea is that you can feed the parser some information,
which makes it aware of what information it is supposed to look for
as well as how to return the data.
As this parser only iterates over the HTML once, it "SHOULD" be faster
than using Beautifulsoup, but this is untested.
"""

from HTMLParser import HTMLParser
from bs4 import UnicodeDammit


class GenericHTMLParser(HTMLParser):
    """
    This class extends Pythons HTMLParser, with a framework that lets the
    user define what the parser is supposed to look for, as well as how to
    return it.

    All public methods, except for parse, are overwritten from HTMLParser
    """

    def __init__(self, parsing_pattern):
        """

        This function initializes the parser

        :param parsing_pattern: A list that describes how html should be parsed
        :type parsing_pattern: list
        """
        HTMLParser.__init__(self)
        self.__tag_result = {}
        self.__prev_tag_stack = []
        self.__current_tags = parsing_pattern
        self.__tag_counter = 0
        self.__getdata = False
        self.__found_tag = None

    def reset(self):
        """

        function to reset parser, calls super reset and cleans up variables

        .. note::
            Overwritten method from HTMLParser, should not be called directly.
        """
        HTMLParser.reset(self)
        self.__tag_result = {}
        self.__prev_tag_stack = []
        self.__tag_counter = 0
        self.__getdata = False
        self.__found_tag = None

    # Parse the contents of a file or file-like object
    def parse(self, html_text):
        """

        Parse the provided html_text

        :param html_text: A string of HTML
        :type html_text: str
        :returns: dict -- parsed data
        """
        # reset parser to original state
        self.reset()
        # Use Beautiful Soup UnicodeDammit to decode to unicode
        decoded_html = UnicodeDammit(html_text, is_html=True)
        # Feed parser
        self.feed(decoded_html.unicode_markup)
        return self.__tag_result

    def handle_starttag(self, tag, attrs):
        """

        Handle start of a tag.

        :param tag: Lowercased tag name
        :type tag: str
        :param attrs: A list of tuples with attributes in the tag.
        :type attrs: list
        :raises: ParseFailError

        .. note::
            Overwritten method from HTMLParser, should not be called directly.
        """
        # if tag is a break tag call add_to_data function,
        # which adds <br>, if we are looking for data and is in same tag
        if self.__found_tag is not None\
            and self.__found_tag.get('keep_break_tags', False)\
            and tag == 'br':
            self.__add_to_data('<br>')
        # if a subtag has been found in this iteration this var is set to true
        new_tag_found = False
        # if the tag is the same that we are looking for,
        # and it has the same attributes, continue
        for current_tag in self.__current_tags:
            # if the tag is the one we are looking for
            if current_tag['tag'] == tag\
                    and (current_tag.get('attributes', None) in attrs\
                    or current_tag.get('attributes', None) is None):
                # save old context
                self.__prev_tag_stack.append({
                    'previous_tags': self.__current_tags,
                    'tag_counter': self.__tag_counter,
                    'found_tag': self.__found_tag,
                    'tag_result': self.__tag_result,
                    'get_data': self.__getdata
                })

                new_tag_found = True
                self.__tag_counter = 1
                self.__found_tag = current_tag
                # create a dict to store return data for this tag
                self.__tag_result = {}

                # set getdata value, so the handle_data function is aware
                # that it needs to acquire the data from the tag
                if current_tag.get('data_target_name', None) is not None:
                    self.__getdata = True
                # acquire information from attributes
                # but only if there is something to acquire
                if current_tag.get('attribute_target_name', None) is not None\
                    and len(attrs) > 0:
                    self.__acquire_attribute_data(current_tag, attrs)
                # If there is subtags, next tags is set to them,
                # actual processing is done in the handle_data method.
                self.__current_tags = current_tag.get('subtags', [])
                # As the tag has been found, break for loop
                break
        # tag counter, this helps track when the tag ends
        if not new_tag_found and self.__found_tag is not None\
            and self.__found_tag['tag'] == tag:
            self.__tag_counter += 1

    def handle_data(self, data):
        """

        Handle data in between a tag

        :param data: Text that is not classified as HTML
        :type data: str

        .. note::
            Overwritten method from HTMLParser, should not be called directly.
        """
        self.__add_to_data(data)

    def handle_charref(self, name):
        """

        Handle hex and numerical characters

        :param name: Text that is not classified as HTML
        :type name: str

        .. note::
            Overwritten method from HTMLParser, should not be called directly.
            Code to convert name to character was copied from Pythons
            HTMLParser example http://docs.python.org/2/library/htmlparser.html
        """
        if self.__getdata and self.__tag_counter == 1:
            if name.startswith('x'):
                name = unichr(int(name[1:], 16))
            else:
                name = unichr(int(name))
            self.__add_to_data(name)

    def handle_endtag(self, tag):
        """

        Handle end of a tag.

        :param tag: Lowercased tag name
        :type tag: str

        .. note::
            Overwritten method from HTMLParser, should not be called directly.
        """
        # if the tag is the one we are looking for, decrement counter
        if self.__found_tag is not None and tag == self.__found_tag['tag']:
            self.__tag_counter -= 1
            # if the counter is 0, it means the end of the scope of this target
            # subtag results is added to results,
            # and tag result added to main results
            if self.__tag_counter == 0:
                subtag_result = self.__tag_result
                subtag = self.__found_tag
                # get the old context
                prev_tag = self.__prev_tag_stack.pop()
                # restore the results from the outer tag
                self.__tag_result = prev_tag['tag_result']
                # add the result of the sub tag to the outer tag
                if subtag.get('ignore', False):
                    if subtag.get('multiple_tags', False):
                        # there will only ever be one subtag_target
                        for subtag_target in subtag_result:
                            try:
                                self.__tag_result[subtag_target].\
                                append(subtag_result[subtag_target])
                            except KeyError:
                                self.__tag_result[subtag_target] = []
                                self.__tag_result[subtag_target].\
                                append(subtag_result[subtag_target])
                    else:
                        self.__tag_result = subtag_result
                else:
                    self.__add_subtag_data_to_result(subtag_result)
                # restore context
                self.__current_tags = prev_tag['previous_tags']
                self.__found_tag = prev_tag['found_tag']
                self.__tag_counter = prev_tag['tag_counter']
                self.__getdata = prev_tag['get_data']

    def __acquire_attribute_data(self, pattern_tag, parsed_tag_attributes):
        """

        Adds data from an attribute to result

        :param pattern_tag: dict from the parsers tag_pattern
        :type pattern_tag: dict
        :param parsed_tag_attributes: list of tuples with attributes and values
        :type parsed_tag_attributes: list
        :raises: ParseFailError
        """
        # if we only want to acquire information from one
        # attribute, store without a list
        return_attributes = pattern_tag.get('return_attributes', [])
        if len(return_attributes) == 1:
            for attribute in parsed_tag_attributes:
                # if the attribute key is the same
                if attribute[0] == return_attributes[0]:
                    self.__tag_result[pattern_tag\
                        ['attribute_target_name']] = attribute[1]
        # if we want to return the values
        # of more than one attribute, store in a lsit
        elif len(return_attributes) > 1:
            returned_attributes = []
            for returnattribute in return_attributes:
                for attribute in parsed_tag_attributes:
                    # if attribute is the same as the
                    # return attribute, append its value
                    if attribute[0] == returnattribute:
                        returned_attributes.append(attribute[1])
            # if there is something to return, return it
            if len(returned_attributes) > 0:
                self.__tag_result[pattern_tag[\
                'attribute_target_name']] = returned_attributes
            # if there is no result raise an exception
            # since there should alway be in the tag, that
            # is being looked for.
            else:
                raise ParseFailError('This tag does not have \
                    the attribute that is being looked for')
        # if we want to return ALL attribute keys and values
        else:
            attr_amount = len(parsed_tag_attributes)
            if attr_amount == 1:
                self.__tag_result[pattern_tag\
                ['attribute_target_name']] = parsed_tag_attributes[0]
            else:
                self.__tag_result[pattern_tag\
                ['attribute_target_name']] = parsed_tag_attributes


    def __add_to_data(self, value):
        """

        Adds a value to the data return value

        :param value: String to add to data result.
        :type value: str
        """
        # if we want to get data, and in same tag
        if self.__getdata and self.__tag_counter == 1:
            # add data information to result
            prev_data = self.__tag_result.\
                get(self.__found_tag['data_target_name'], '')
            self.__tag_result[self.__found_tag['data_target_name']] = \
                prev_data + value

    def __add_subtag_data_to_result(self, value):
        """

        Adds data from a subtag to the end result

        :param value: Dict with results from a subtag,
                        has same structure as the end result
        :type value: dict
        """
        tag_target_name = self.__found_tag.get('tag_target_name', None)
        # this function relies on found_tag not having been reset to outer tag
        # and tag_result having been set to outer tag
        if self.__found_tag.get('multiple_tags', False):
            # if there is only one type of result in tag, ignore tag_target
            if len(value) == 1:
                for single_result in value:
                    # change tag_target_name to the key
                    # of whatever is in the results
                    tag_target_name = single_result
                    # change the value, to be the value of the key
                    value = value[single_result]
            try:
                self.__tag_result[tag_target_name].append(value)
            except KeyError:
                self.__tag_result[tag_target_name] = []
                self.__tag_result[tag_target_name].append(value)
        else:
            if len(value) == 1:
                for single_result in value:
                    self.__tag_result[single_result] = value[single_result]
            else:
                self.__tag_result[tag_target_name] = value


class ParseFailError(Exception):
    """
    Simple exception class that passes all responsibility to super class.
    """
    pass
