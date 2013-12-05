#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: application

This module contains all the views for the web application,
defined by Flask (http://flask.pocoo.org/) routing.
"""

from flask import Flask, jsonify, render_template, request
from tp.data_collection_controllers.data_collector import ratings_for_company

app = Flask(__name__)


@app.route('/ajax/review/', methods=['POST'])
def get_review_page_information():
    """

    For each company page, this function returns the differentiated scores
    in the topics 'rma', 'price', 'delivery' and 'general'.

    :returns: json -- containing scores.
    """

    if request.method == "POST":
        url = request.form.get('url', False)
        ratings = ratings_for_company(url)
        ratings = dict(ratings)
        if url:
            return jsonify(rma_score=ratings.get('rma', 0),
                           price_score=ratings.get('price', 0),
                           delivery_score=ratings.get('delivery', 0),
                           general_score=ratings.get('general', 0))
        else:
            return jsonify(error='url not available')
    return jsonify(error='HTTP method wrong')


@app.route('/')
def index():
    """

    Returns the index page of the web application

    :returns: HTML template
    """
    return render_template('index.html')
