#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: util

"""

from tp.job_controllers import TERMINATED
from tp.job_controllers import MIN_START_TIME, MAX_START_TIME, JOBS_PER_HOUR
from tp.orm.models import Job
from time import time
from datetime import datetime, timedelta

JOB_FREQUENCY = 60 * 60 / JOBS_PER_HOUR


def generate_starttime():
    """
    Utility function to find and return the next available time slot
    in the job queue.

    :returns: int -- unix time stamp
    """
    last_running_job = Job.select().where(Job.status != TERMINATED)\
        .order_by(Job.start_time.desc()).first()
    if last_running_job:
        time_of_last_running = last_running_job.start_time
    else:
        time_of_last_running = int(time())

    next_job_unix = time_of_last_running + JOB_FREQUENCY
    next_job = datetime.fromtimestamp(next_job_unix)
    hour = int(next_job.strftime('%H'))
    minute = int(next_job.strftime('%M'))
    seconds = int(next_job.strftime('%S'))

    delta_hours = 0
    delta_days = 0
    delta_minutes = 0

    if MIN_START_TIME > hour > MAX_START_TIME\
            or MAX_START_TIME > hour < MIN_START_TIME < MAX_START_TIME:
        # Samme dag ved start tidspunktet
        delta_hours = (MIN_START_TIME - hour)
        delta_minutes = -minute
    elif MIN_START_TIME < hour >= MAX_START_TIME > MIN_START_TIME:
        # Skal køre på min start tid næste dag, hvis ikke
        # min start er større end max start.
        delta_hours = (MIN_START_TIME - hour)
        delta_days = 1
        delta_minutes = -minute
    else:
        pass

    next_job = next_job + timedelta(days=delta_days,
                                    hours=delta_hours,
                                    minutes=delta_minutes,
                                    seconds=-seconds)
    return int(next_job.strftime('%s'))
