#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: create_job_for_company_rating

"""

from tp.orm.models import Company, Job, Review
from tp.job_controllers import IN_QUEUE, TYPE_RATING
from tp.job_controllers.util import generate_starttime


class NoReviewException(Exception):
    """
    Simple exception class that passes all responsibility to super class.
    """
    pass


def create_job_for_company_rating():
    """
    Function to create a job for calculating the rating for all companies.

    .. note:: The reviews needs to be received before this function works.
    """

    for company in Company.select():
        if Review.select(Review.company).where(
                Review.company == company.company).count() > 0:
            start_time = generate_starttime()
            Job(start_time=start_time,
                status=IN_QUEUE,
                target=company.company,
                type=TYPE_RATING).save()
        else:
            raise NoReviewException()
            #todo: handle NoReviewException

if __name__ == '__main__':
    create_job_for_company_rating()
