#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: create_job_for_company_rating

"""

from tp.orm.models import Company, Job, Review
from tp.job_controllers import IN_QUEUE, TYPE_RATING
from tp.job_controllers.util import generate_starttime
from tp.logging.logger import get_logger as log


def create_job_for_company_rating():
    """
    Function to create a job for calculating the rating for all companies.

    .. note:: The reviews needs to be received before this function works.
    """

    for company in Company.select():
        if Review.select(Review.company).where(
                Review.company == company.company).count() > 0:
            #todo: maybe set another threshold than 0
            start_time = generate_starttime()
            Job(start_time=start_time,
                status=IN_QUEUE,
                target=company.company,
                type=TYPE_RATING).save()
        else:
            log().info("The company {}'s number of reviews doesn't "
                       "meet the threshold".format(company.domain_name))

if __name__ == '__main__':
    create_job_for_company_rating()
