#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: Models


"""

from peewee import MySQLDatabase, Model, PrimaryKeyField, ForeignKeyField
from peewee import IntegerField, CharField, TextField, FloatField


DB = MySQLDatabase('tp', **{'passwd': 'SKAjdlkwq3nsjd3if993',
                            'user': 'tp'})


class UnknownFieldType(object):
    """
    Simple class to be used if a field does not exists.
    """
    pass


class BaseModel(Model):
    """
    Simple class used to keep track of Meta data which is equal for all classes.
    """

    class Meta(object):
        """
        Simple class to keep track of database connection
        """
        database = DB


class Category(BaseModel):
    """
    Data class for Category object referring to `tp.category` in the database
    """
    category = PrimaryKeyField(db_column='category_id')
    name = CharField()
    tp_category = CharField(db_column='tp_category_id')
    url = CharField()

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'category'


class Company(BaseModel):
    """
    Data class for Company object referring to `tp.company` in the database
    """
    company = PrimaryKeyField(db_column='company_id')
    domain_name = CharField()
    review_count = IntegerField()
    reviews_updated_at = IntegerField()

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'company'


class CompanyCategory(BaseModel):
    """
    Data class for CompanyCategory object referring
    to `tp.company_category` in the database
    """
    category = ForeignKeyField(db_column='category_id', rel_model=Category)
    company_category = PrimaryKeyField(db_column='company_category_id')
    company = ForeignKeyField(db_column='company_id', rel_model=Company)

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'company_category'


class CategoryPosition(BaseModel):
    """
    Data class for CategoryPosition object referring
    to `tp.category_position` in the database
    """
    company_category = ForeignKeyField(db_column='company_category_id',
                                       rel_model=CompanyCategory)
    created_at = IntegerField()
    group = CharField()
    position = IntegerField()

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'category_position'


class User(BaseModel):
    """
    Data class for User object referring to `tp.user` in the database
    """
    gender = CharField(null=True)
    review_count = IntegerField()
    user = PrimaryKeyField(db_column='user_id')

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'user'


class Review(BaseModel):
    """
    Data class for Review object referring to `tp.review` in the database
    """
    company = ForeignKeyField(db_column='company_id', rel_model=Company)
    content = TextField(null=True)
    created_at = IntegerField()
    rating = IntegerField()
    review = PrimaryKeyField(db_column='review_id')
    title = CharField(null=True)
    tp_review = IntegerField(db_column='tp_review_id')
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'review'


class ComputedReviewRating(BaseModel):
    """
    Data class for ComputedReviewRating object referring
    to `tp.computed_review_rating` in the database
    """
    delivery_value = FloatField(null=True)
    price_value = FloatField(null=True)
    review = ForeignKeyField(db_column='review_id', rel_model=Review)
    rma_value = FloatField(null=True)
    updated_at = IntegerField()

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'computed_review_rating'


class Job(BaseModel):
    """
    Data class for Job object referring to `tp.job` in the database
    """
    job = IntegerField(db_column='job_id', primary_key=True)
    start_time = IntegerField()
    status = CharField()
    target = IntegerField()
    type = CharField()

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'job'


class Rating(BaseModel):
    """
    Data class for Rating object referring to `tp.rating` in the database
    """
    company = ForeignKeyField(db_column='company_id', rel_model=Company)
    created_at = IntegerField()
    group = CharField()
    value = FloatField()

    class Meta(object):
        """
        Simple class to define table name in database
        """
        db_table = 'rating'
