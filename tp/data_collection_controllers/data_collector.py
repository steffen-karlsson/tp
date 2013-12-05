#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tp.orm.models import Company, Review, User
from tp.orm.models import Rating, CompanyCategory, CategoryPosition
from datetime import datetime
from peewee import DoesNotExist
from tp.data_collection_controllers.util.downloader import download
from tp.data_collection_controllers.util.downloader import DownloadFailError
from tp.data_collection_controllers.parser_factory \
    import _create_category_parser
from tp.data_collection_controllers.parser_factory \
    import _create_review_parser
from tp.data_collection_controllers.parser_factory \
    import _create_review_parser_first
from tp.data_collection_controllers.util.helpers import to_utc_timstamp, now

TP_BASEURL = 'http://www.trustpilot.dk'
CATEGORY_AJAX_URL = "{}/categories/ajaxresults".format(TP_BASEURL)

CREATED_AT_FORMAT = '%Y-%m-%dT%H:%M:%S'
NONE = -1
COMPANIES_PER_PAGE = 20


def __get_review_url(company_address, page=None):
    return '{}?page={}'.format(company_address, 1 if page is None else page)


def __get_category_url(category_id, page):
    return '{}?id={}&page={}'.format(CATEGORY_AJAX_URL,
                                     category_id,
                                     page)


def reviews_for_company(company):
    utc_now = to_utc_timstamp(now())
    update_time = company.reviews_updated_at
    Company.update(reviews_updated_at=utc_now).where(
        Company.company == company.company).execute()

    review_count = float('inf')
    page_count = 1
    __html_parser = _create_review_parser()
    # Looping until the review count is 0. Decreasing by number of review
    # At the page pr round.
    while review_count >= 0:
        try:
            __url = __get_review_url(company.domain_name.encode('utf-8'),
                                     page=page_count)
            __response = download(__url)
            # If its the first page, the use the custom parser,
            # which is paring the review count and the tp score,
            # other than than the reviews too.
            if page_count == 1:
                __html_parser_first = _create_review_parser_first()
                __parsed_data = __html_parser_first.parse(__response.read())
                review_count = int(__parsed_data.get('review_count', 0))
                tp_score = float(__parsed_data.get('tp_score', 0))

                # Updating the company with the review count
                Company.update(review_count=review_count).where(
                    Company.company == company.company).execute()
                # Creating a new Rating object related to the company
                # with the tp_score.
                Rating(company=company.company,
                       created_at=utc_now,
                       group='tp',
                       value=tp_score).save()
            else:
                __parsed_data = __html_parser.parse(__response.read())

            reviews = __parsed_data.get('reviews', None)
            # Safety check if there is any reviews
            if reviews:
                for review in reviews:
                    if __save_review(review, company, update_time):
                        # If save review return true, means that
                        # the review count should be decreased
                        review_count -= 1
                    else:
                        # False means that we have the rest of the reviews
                        return
                page_count += 1
            else:
                # No more reviews
                return
        except DownloadFailError:
            #todo: handle DownloadFailError
            pass


def companies_for_category(category):
    page_count = 1
    __html_parser = _create_category_parser()
    while True:
        try:
            __url = __get_category_url(category.tp_category, page_count)
            __response = download(__url)
            __parsed_data = __html_parser.parse(__response.read())
            # If the page is empty the parser returns an empty dict.
            # This only happens when (no.companies in category) % 20 == 0
            if len(__parsed_data) == 0:
                break
            companies = __parsed_data.get('companies', {})
            for company in companies:
                __save_company(company, category)
            # If len of categories is less than 20, means we reached
            # last "page" in the category
            if len(companies) < COMPANIES_PER_PAGE:
                break
            page_count += 1
        except DownloadFailError:
            #todo: handle DownloadFailError
            pass


def ratings_for_company(domain_name):
    company = Company.get(Company.domain_name == domain_name)
    ratings = Rating.select().where(Rating.company == company.company)
    for rating in ratings:
        if rating.group != 'tp':
            yield (rating.group, rating.value)


def __save_review(data, company, update_time):
    created_at = str(data['created_at']).split('.')[0]
    tp_review_id = data['tp_review_id']
    local_unixtimestamp = datetime.strptime(
        created_at, CREATED_AT_FORMAT).strftime('%s')
    created_at = to_utc_timstamp(local_unixtimestamp)

    if created_at < int(update_time):
        return False
    try:
        Review.get(Review.tp_review == tp_review_id)
        return False
    except DoesNotExist:
        user = __save_user(data['user'])
        Review(company=company.company,
               content=data['content'],
               created_at=created_at,
               rating=data['rating'],
               title=data['title'],
               tp_review=tp_review_id,
               user=user.user).save()
        return True


def __save_user(data):
    review_count = int(data['review_count'].split()[0])
    #name = data['author']
    #todo: name used to find gender of user
    user = User(gender='und',
                review_count=review_count)
    user.save()
    return user


def __save_company(data, category):
    domain_name = TP_BASEURL + data['url']
    try:
        company = Company.get(Company.domain_name == domain_name)
        company_received = True
    except DoesNotExist:
        # The convention is that if the variable
        # doesn't exists the value is NONE(-1)
        company = Company(domain_name=domain_name,
                          review_count=NONE,
                          reviews_updated_at=NONE)
        company.save()
        company_received = False

    if company_received:
        try:
            company_category = CompanyCategory.get(
                (CompanyCategory.company == company.company) &
                (CompanyCategory.category == category.category))
        except DoesNotExist:
            company_received = False
    if not company_received:
        company_category = CompanyCategory(category=category.category,
                                           company=company.company)
        company_category.save()

    utc_now = to_utc_timstamp(now())
    position = data['ranking'].strip().split('.')[0]
    CategoryPosition(company_category=company_category.company_category,
                     created_at=utc_now,
                     group='tp',
                     position=position).save()
