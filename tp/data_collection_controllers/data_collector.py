from tp.orm.models import Company, Review, User
from tp.orm.models import Rating, Category, CategoryPosition
from datetime import datetime
from peewee import DoesNotExist
from time import time

TP_BASEURL = 'http://www.trustpilot.dk/'
REVIEW_BASEURL = "{}review".format(TP_BASEURL)
CATEGORY_BASEURL = "{}categories".format(TP_BASEURL)

CREATED_AT_FORMAT = '%Y-%m-%dT%H:%M:%S'
NONE = -1

def get_review_url(company_address, page=None):
    return '{}{}?page={}'.format(REVIEW_BASEURL, company_address,
                                 1 if page is None else page)


def get_category_url(category):
    return '{}{}'.format(CATEGORY_BASEURL, category)


def save_review(data, company):
    created_at = data['created_at']
    tp_review_id = data['tp_review_id']
    local_unixtimestamp = datetime.strptime(created_at, CREATED_AT_FORMAT).strftime('%s')
    created_at = datetime.utcfromtimestamp(float(local_unixtimestamp)).strftime('%s')
    if created_at < company.reviews_updated_at:
        return
    try:
        Review.get(Review.review == tp_review_id)
        return
    except DoesNotExist:
        user = save_user(data['user'])
        Review(company=company.company,
               content=data['content'],
               created_at=created_at,
               rating=data['rating'],
               title=data['title'],
               tp_review=tp_review_id,
               user=user.user).save()


def save_user(data):
    review_count = int(data['review_count'].split()[0])
    name = data['name']
    #todo: name used to find gender of user
    user = User(gender='und',
                review_count=review_count)
    user.save()
    return user


def __save_company(data, category_name):
    domain_name = data['url']
    domain_name = domain_name.split(REVIEW_BASEURL)[1]\
        if domain_name.startswith(REVIEW_BASEURL)\
        else domain_name.split('/review/')[1]\
        if domain_name.startswith('/review/')\
        else ""
    domain_name = domain_name\
        if domain_name.startswith('www.')\
        else "www.{}".format(domain_name)

    try:
        company = Company.get(Company.domain_name == domain_name)
        company_received = True
    except DoesNotExist:
        # The convention is that if the variable
        # doesn't exists the value is NONE(-1)
        company = Company(domain_name=domain_name,
                          review_count=NONE,
                          reviews_updated_at=NONE).save()
        company_received = False

    if company_received:
        try:
            company_category = Category.get(
                (Category.company == company.company) &
                (Category.category_name == category_name))
        except DoesNotExist:
            company_received = False
    if not company_received:
        company_category = Category(category_name=category_name,
                                    company=company.company).save()

    utc_now = to_utc_timstamp(now())
    position = data['ranking'].strip().split('.')[0]
    CategoryPosition(category=company_category.category,
                     created_at=utc_now,
                     group='tp',
                     position=position).save()


def __update_company(data, company):
    Company.update(review_count=data['review_count']).where(
        Company.company == company.company)
    utc_now = to_utc_timstamp(now())
    Rating(company=company.company,
           created_at=utc_now,
           group='tp',
           value=data['tp_score']).save()


def to_utc_timstamp(timestamp):
    return datetime.utcfromtimestamp(float(timestamp)).strftime('%s')


def now():
    return int(str(time()).split('.')[0])
