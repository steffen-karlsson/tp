from urllib2 import urlopen, Request


def download(url):
    req = Request(url)
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            return response
    except ValueError:
        pass
    raise DownloadFailError()


class DownloadFailError(Exception):
    pass

