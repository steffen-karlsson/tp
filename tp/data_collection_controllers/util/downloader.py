#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: downloader

"""

from urllib2 import urlopen, Request, quote, HTTPError


def download(url):
    """

    Downloading the url and returns a HTML response object,
    if the response code is 200 else a DownloadFailError exception.

    :param url: the url to be downloaded
    :type url: str
    :raises: DownloadFailError
    :returns: HTML response object
    """

    req = Request(quote(url, safe=':/?&='))
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            return response
    except (ValueError, HTTPError), e:
        pass
    raise DownloadFailError(e)


class DownloadFailError(Exception):
    """
    Simple exception class that passes all responsibility to super class.
    """
    pass

