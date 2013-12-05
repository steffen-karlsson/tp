#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: job_executor

"""

from tp.orm.models import Job, Category, Company, Review
from tp.data_collection_controllers.util.helpers import to_utc_timstamp, now
from tp.data_collection_controllers.data_collector \
    import companies_for_category
from tp.data_collection_controllers.data_collector \
    import reviews_for_company
from tp.data_collection_controllers.data_collector \
    import rating_for_company
from tp.job_controllers import IN_QUEUE, EXECUTING, TERMINATED
from tp.job_controllers import TYPE_CATEGORY, TYPE_COMPANY, TYPE_RATING
from peewee import DoesNotExist


class JobTypeNotFoundException(Exception):
    """
    Simple exception class which is being raised
    if the job type doesn't exists.
    """
    pass


def process_jobs():
    """

    This function finds jobs from the database, with a starting time stamp
    older than now and executes them.
    """
    utc_now = to_utc_timstamp(now())
    try:
        jobs = Job.select().where((Job.start_time <= utc_now)
                                  & (Job.status == IN_QUEUE)
                                  ).order_by(Job.start_time.asc())
    except DoesNotExist:
        return
    job_count = jobs.count()
    if job_count == 0:
        return
    if job_count > 1:
        #todo: something went wrong! Only one job at a time
        pass

    # Setting status of jobs to executing
    # to prevent executing the job more than once.
    for job in jobs:
        job.status = EXECUTING
        job.save()

    for job in jobs:
        __execute_job(job)


def __execute_job(job):
    """

    Function for executing a job and saving
    state of the job depending on the type.

    :param job: a Job which is ready to be executed
    :type job: Job
    """
    _type = job.type
    if _type == TYPE_CATEGORY:
        category_id = job.target
        category = Category.get(Category.category == category_id)
        companies_for_category(category)
    elif _type == TYPE_COMPANY:
        company_id = job.target
        company = Company.get(Company.company == company_id)
        reviews_for_company(company)
    elif _type == TYPE_RATING:
        company_id = job.target
        rating_for_company(company_id)
    else:
        raise JobTypeNotFoundException()

    #Updating status to terminated
    job.status = TERMINATED
    job.save()


if __name__ == '__main__':
    process_jobs()
