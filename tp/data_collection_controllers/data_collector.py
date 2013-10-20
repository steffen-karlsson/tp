from tp.orm.models import Company, Review, User
from datetime import datetime
from peewee import DoesNotExist

TP_BASEURL = 'http://www.trustpilot.dk/'
REVIEW_BASEURL = "{}review".format(TP_BASEURL)
CATEGORY_BASEURL = "{}categories".format(TP_BASEURL)

CREATED_AT_FORMAT = '%Y-%m-%dT%H:%M:%S'


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


def __update_company(data, company):
    Company.update(review_count=data['review_count']).where(
        Company.company == company.company)
    utc_now = to_utc_timstamp(now())
    Rating(company=company.company,
           created_at=utc_now,
           group="tp",
           value=data['tp_score']).save()


def to_utc_timstamp(timestamp):
    return datetime.utcfromtimestamp(float(timestamp)).strftime('%s')


def now():
    return int(str(time()).split('.')[0])