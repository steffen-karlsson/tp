#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: application

This module contains all the views for the web application,
defined by Flask (http://flask.pocoo.org/) routing.
"""

from flask import Flask, jsonify, render_template, request
from tp.orm.models import Company, Rating
from peewee import DoesNotExist

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
        if url:
            try:
                company = Company.get(Company.domain_name == url)
                ratings_statement = Rating.select().where(
                    Rating.company == company.company)
                if ratings_statement.count() > 0:
                    ratings = {}
                    for rating in ratings_statement:
                        if rating.group != 'tp':
                            ratings[rating.group] = rating.value
                    return jsonify(rma_score=ratings.get('rma', 0),
                                   price_score=ratings.get('price', 0),
                                   delivery_score=ratings.get('delivery', 0),
                                   general_score=ratings.get('general', 0),
                                   status=10)
                return jsonify(status=20)
            except DoesNotExist:
                return jsonify(status=21)

    return index()


@app.route('/')
def index():
    """

    Returns the index page of the web application

    :returns: HTML template
    """
    return render_template('index.html')