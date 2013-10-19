
TP_BASEURL = 'http://www.trustpilot.dk/'
REVIEW_BASEURL = "{}review".format(TP_BASEURL)
CATEGORY_BASEURL = "{}categories".format(TP_BASEURL)


def get_review_url(company_address, page=None):
    return '{}{}?page={}'.format(REVIEW_BASEURL, company_address,
                                 1 if page is None else page)


def get_category_url(category):
    return '{}{}'.format(CATEGORY_BASEURL, category)
