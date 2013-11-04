#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tp.orm.models import Job, Category, Company
from util.helpers import to_utc_timstamp, now
from data_collector import companies_for_category, reviews_for_company

IN_QUEUE = 'in-queue'
EXECUTING = 'executing'
TERMINATED = 'terminated'

TYPE_CATEGORY = 'category'
TYPE_COMPANY = 'company'


class JobTypeNotFoundException(Exception):
    pass


def process_jobs():
    utc_now = to_utc_timstamp(now())
    jobs = Job.get((Job.start_time <= utc_now)
                   & (Job.status == IN_QUEUE)).order_by(Job.start_time.asc())

    job_count = len(jobs)
    if job_count < 0:
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
    _type = job.type
    if _type is TYPE_CATEGORY:
        category_id = job.target
        category = Category.get(Category.category == category_id)
        companies_for_category(category)
    elif _type is TYPE_COMPANY:
        company_id = job.target
        company = Company.get(Company.company == company_id)
        reviews_for_company(company)
    else:
        raise JobTypeNotFoundException()

    #Updating status to terminated
    job.status = TERMINATED
    job.save()


if __name__ == '__main__':
    process_jobs()