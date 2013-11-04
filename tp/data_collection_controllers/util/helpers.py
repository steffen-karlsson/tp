#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from time import time


def to_utc_timstamp(timestamp):
    return datetime.utcfromtimestamp(float(timestamp)).strftime('%s')


def now():
    return int(str(time()).split('.')[0])