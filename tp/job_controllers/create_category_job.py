#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tp.job_controllers import IN_QUEUE, TYPE_CATEGORY
from tp.orm.models import Job, Category
from generate_job_starttime import generate


def create_job_for_category(category):
    start_time = generate()
    Job(start_time=start_time,
        status=IN_QUEUE,
        target=category.category,
        type=TYPE_CATEGORY).save()


if __name__ == '__main__':
    for category in Category.select():
        create_job_for_category(category.category)
