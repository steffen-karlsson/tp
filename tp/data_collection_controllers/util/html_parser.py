#!/usr/bin/env python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

##
# "Generic" SAX-styled HTML-parser
# Idea is that you can feed the parser some information, 
# which makes it aware of what information it is supposed to look for as well as to what to return it as.
# As this parser only iterates over the HTML once, it "SHOULD" be faster than using Beautifulsoup, but this is untested.
#
#
# v. 0.2.0
# By Rune Thor Mårtensson
# TODO: 
# - Sphinx documentation
# - Make sure it works with tags without ends (br, hr and so on)
# - Improve performance
# - Implement a proper exception
##


class HTMLParser(HTMLParser):

    def __init__(self, parsing_pattern):
        HTMLParser.__init__(self)
        self.__tag_result = {}
        self.__prev_tag_stack = []
        self.__current_tags = parsing_pattern
        self.__tag_counter = 0
        self.__next_tags = None
        self.__getdata = False
        self.__tag_found = False
        self.__found_tag = None

    # Parse the contents of a file or file-like object
    def parse(self, file_reference):
        self.feed(self.unescape(file_reference.read().decode('utf-8')))
        return self.__tag_result

    def handle_starttag(self, tag, attrs):
        # if a subtag has been found in this iteration this var is set to true
        new_tag_found = False
        # if the tag is the same that we are looking for, 
        # and it has the same attributes, continue
        for current_tag in self.__current_tags:
            if current_tag['tag'] == tag:
                # if the tag is the one we are looking for
                if current_tag['attributes'] in attrs or current_tag['attributes'] is None:
                    # save old context
                    self.__prev_tag_stack.append({
                        'previous_tags' : self.__current_tags, 
                        'tag_counter' : self.__tag_counter, 
                        'found_tag' : self.__found_tag,
                        'tag_found' : self.__tag_found,
                        'tag_result': self.__tag_result
                    })

                    new_tag_found = True
                    self.__tag_counter = 1
                    self.__tag_found = True
                    self.__found_tag = current_tag
                    # create a dict to store return data for this tag
                    self.__tag_result = {}                    
                    self.__next_tags = None

                    # set getdata value, so the handle_data function is aware
                    # that it needs to acquire the data from the tag
                    if current_tag['data_target_name'] is not None and current_tag['ignore'] == False:
                        self.__getdata = True
                    # acquire information from attributes
                    if current_tag['attribute_target_name'] is not None and current_tag['ignore'] == False:
                        # if we only want to acquire information from one 
                        # attribute, store without a list
                        if len(current_tag['returnattributes']) == 1:
                            for attribute in attrs:
                                # if the attribute key is the same
                                if attribute[0] == current_tag['returnattributes'][0]:
                                    self.__tag_result[current_tag['attribute_target_name']] = attribute[1]
                        # if we want to return the values of more than one attribute
                        elif len(current_tag['returnattributes']) > 1:
                            returned_attributes = []
                            for returnattribute in current_tag['returnattributes']:
                                for attribute in attrs:
                                    # if attribute is the same as the return attribute, append its value
                                    if attribute[0] == returnattribute:
                                        returned_attributes.append(attribute[1])
                            # if there is something to return, return it
                            if len(returned_attributes) > 0:
                                self.__tag_result[current_tag['attribute_target_name']] = returned_attributes
                            else:
                                raise Exception('This tag does not have the one that is being looked for')
                        # if we want to return ALL attribute keys and values
                        else:
                            attr_amount = len(attrs)
                            if attr_amount == 1:
                                self.__tag_result[current_tag['attribute_target_name']] = attrs[0]
                            elif attr_amount > 1:
                                self.__tag_result[current_tag['attribute_target_name']] = attrs
                            else:
                                self.__tag_result[current_tag['attribute_target_name']] = None
                    # If there is subtags, next tags is set to them, 
                    # actual processing is done in the handle_data method.
                    self.__next_tags = current_tag['subtags']
        # if the tag is the same as the one that was found, increment 
        # tag counter, this helps track when the tag ends
        if not new_tag_found and self.__found_tag is not None and self.__found_tag['tag'] == tag:
            self.__tag_counter += 1

    def handle_data(self, data):
        if self.__getdata:
            # add data information to result
            self.__tag_result[self.__found_tag['data_target_name']] = data
            self.__getdata = False
        if self.__next_tags is not None:
            # set __current_tags to the subtags of the found tag
            # this will make it search for subtag data
            self.__current_tags = self.__next_tags

    def handle_endtag(self, tag):
        # if the tag is the one we are looking for, decrement counter
        if self.__tag_found and tag == self.__found_tag['tag']:
            self.__tag_counter -= 1
            # if the counter is 0, it means the end of the scope of this target
            # subtag results is added to results, and tag result added to main results
            if self.__tag_counter == 0:      
                subtag_result = self.__tag_result
                subtag = self.__found_tag
                # get the old context
                prev_tag = self.__prev_tag_stack.pop()
                # restore the results from the outer tag
                self.__tag_result = prev_tag['tag_result']
                # add the result of the sub tag to the outer tag
                if subtag['ignore'] == True:
                    if subtag['multiple_tags']:
                        # there will only ever be one subtag_target
                        for subtag_target in subtag_result:
                            try:
                                self.__tag_result[subtag_target].append(subtag_result[subtag_target])
                            except KeyError:
                                self.__tag_result[subtag_target] = []
                                self.__tag_result[subtag_target].append(subtag_result[subtag_target])
                    else:
                        self.__tag_result = subtag_result
                else:
                    self.__add_subtag_data_to_result(subtag_result)
                # restore context
                self.__tag_found = prev_tag['tag_found']
                self.__current_tags = prev_tag['previous_tags']
                self.__found_tag = prev_tag['found_tag']
                self.__tag_counter = prev_tag['tag_counter']

    def __add_subtag_data_to_result(self,value):
        tag_target_name = self.__found_tag['tag_target_name']
        # this function relies on found_tag not having been reset to outer tag
        # and tag_result having been set to outer tag
        if self.__found_tag['multiple_tags']:
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