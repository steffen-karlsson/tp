#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: create_category_job

"""

from tp.job_controllers import IN_QUEUE, TYPE_CATEGORY
from tp.orm.models import Job, Category
from tp.job_controllers.util import generate_starttime


def create_job_for_category(category):
    """
    Function to create a job for receiving companies from a category.

    :param category: the category where the companies needs to be received.
    :type category: Category
    """
    start_time = generate_starttime()
    Job(start_time=start_time,
        status=IN_QUEUE,
        target=category.category,
        type=TYPE_CATEGORY).save()


if __name__ == '__main__':
    for _category in Category.select():
        create_job_for_category(_category.category)
