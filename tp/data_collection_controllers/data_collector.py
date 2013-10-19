
TP_BASEURL = 'http://www.trustpilot.dk/'
REVIEW_BASEURL = "{}review".format(TP_BASEURL)
CATEGORY_BASEURL = "{}categories".format(TP_BASEURL)


def get_review_url(company_address, page=None):
    return '{}{}?page={}'.format(REVIEW_BASEURL, company_address,
                                 1 if page is None else page)


def get_category_url(category):
    return '{}{}'.format(CATEGORY_BASEURL, category)
def save_user(data):
    review_count = int(data['review_count'].split()[0])
    name = data['name']
    #todo: name used to find gender of user
    user = User(gender='und',
                review_count=review_count)
    user.save()
    return user
