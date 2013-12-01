#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: util

"""

from datetime import datetime
from time import time


def to_utc_timstamp(timestamp):
    """

    Converts local unix time stamp to utc unix time stamp.

    :param timestamp: unix time stamp in local timezone
    :type timestamp: float
    :returns: float -- utc unix time stamp
    """

    return float(datetime.utcfromtimestamp(float(timestamp)).strftime('%s'))


def now():
    """

    Converts local unix time stamp to utc unix time stamp.

    :returns: float -- local unix time stamp of now
    """
    return float(str(time()).split('.')[0])
