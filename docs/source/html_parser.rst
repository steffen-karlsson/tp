Generic HTML parser framework
=============================

.. automodule:: tp.data_collection_controllers.util.html_parser
    :members:
    :private-members:

This is a test of sphinx

Parser pattern
**************

To use the parser framework, it is necessary to define a pattern, which holds information about which tags that should be parsed, and how the returned data should be represented.

The pattern is defined as a list of dicts, each with a number of optional keys and one nonoptional key.

The non optional keys is:

- "tag" - Type string - Indicating a HTML tag

The optional keys are:

- "tag_target_name" - Type string - If more than one type of data is acquired from a tag, this tag is used as a key for the dict which contains the results.
- "attributes" - Single value: set. Multiple values: list of sets - Indicating a HTML tag with attributes, format is ('class', 'name-of-class') if only one attribute, if multiple attributes [('class1', 'name-of-class1'), ('something', 'name-of-class2')]
- "multiple_tags" - Type boolean - Indicating whether or not there is more than one tag.
- "attribute_target_name" - Type string - name of key in returned data
- "return_attributes" - Type list of strings - List of string indicating the attributes that should be returned, if nothing is in the list.
- "data_target_name" - Type string - Name of key in returned data, of data in between the tag and its end.
- "keep_break_tags" - Type boolean - If data is being returned, <br> can be kept.
- "ignore" - Type boolean - Collapse a tree

Example
*******

This example shows how to acquire a 'href' attribute as well as the text from a link tag, that is in a divtag with class "example".

Example HTML:

.. code-block:: html

    <div>
	  <div><a href="example.org">Wrong link</a></div>
	  <div class="example"><a href="tp.runetm.dk">Right link</a></div>
    </div>

Example pattern:

.. code-block:: python

    [{
        'tag':'div',
        'tag_target_name':'Outer div',
        'subtags':
            [{
                'tag':'div',
                'attributes':('class', 'example'),
                'tag_target_name':'Inner div',
                'subtags':
                [{
                    'tag':'a',
                    'return_attributes':['href'],
                    'attribute_target_name':'link',
                    'data_target_name':'link text',
                    'tag_target_name':'link information',
                }]
            }]
    }]

Returned data from example:

.. code-block:: python

    {
        'link information':
            {
                'link': u'tp.runetm.dk',
                'link text': u'Right link'
            }
    }
