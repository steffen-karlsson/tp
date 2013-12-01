#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: create_review_job

"""

from tp.orm.models import CompanyCategory, Job, Category
from tp.job_controllers import IN_QUEUE, TYPE_COMPANY
from tp.job_controllers.util import generate_starttime


def create_job_for_review(category):
    """
    Function to create a job for receiving reviews for
    all companies in a category.

    .. note:: The companies needs to be received before this function works.

    :param category: the category where the reviews needs to be received.
    :type category: Category
    """
    companies = CompanyCategory.select(CompanyCategory.company).where(
        CompanyCategory.category == category.category)
    for company in companies:
        start_time = generate_starttime()
        Job(start_time=start_time,
            status=IN_QUEUE,
            target=company.company,
            type=TYPE_COMPANY).save()

if __name__ == '__main__':
    create_job_for_review(Category.select().where(
        Category.category == 1).get())
