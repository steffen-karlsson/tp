#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import urlopen, Request, quote


def download(url):
    req = Request(quote(url, safe=':/?&='))
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            return response
    except ValueError:
        pass
    raise DownloadFailError()


class DownloadFailError(Exception):
    pass

