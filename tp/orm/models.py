from peewee import *

#database = MySQLDatabase('tp', **{'passwd': 'SKAjdlkwq3nsjd3if993', 'user': 'tp'})
database = MySQLDatabase('tp', **{'passwd': '', 'user': 'root'})


class UnknownFieldType(object):
    pass


class BaseModel(Model):
    class Meta:
        database = database


class Company(BaseModel):
    company = PrimaryKeyField(db_column='company_id')
    domain_name = CharField()
    review_count = IntegerField()
    reviews_updated_at = IntegerField()

    class Meta:
        db_table = 'company'


class Category(BaseModel):
    category = PrimaryKeyField(db_column='category_id')
    category_name = CharField()
    company = ForeignKeyField(db_column='company_id', rel_model=Company)

    class Meta:
        db_table = 'category'


class CategoryPosition(BaseModel):
    category = ForeignKeyField(db_column='category_id', rel_model=Category)
    created_at = IntegerField()
    group = CharField()
    position = IntegerField()

    class Meta:
        db_table = 'category_position'


class User(BaseModel):
    gender = CharField(null=True)
    review_count = IntegerField()
    user = PrimaryKeyField(db_column='user_id')

    class Meta:
        db_table = 'user'


class Review(BaseModel):
    company = ForeignKeyField(db_column='company_id', rel_model=Company)
    content = TextField(null=True)
    created_at = IntegerField()
    rating = IntegerField()
    review = PrimaryKeyField(db_column='review_id')
    title = CharField(null=True)
    tp_review = IntegerField(db_column='tp_review_id')
    user = ForeignKeyField(db_column='user_id', rel_model=User)

    class Meta:
        db_table = 'review'


class ComputedReviewRating(BaseModel):
    delivery_value = FloatField(null=True)
    price_value = FloatField(null=True)
    review = ForeignKeyField(db_column='review_id', rel_model=Review)
    rma_value = FloatField(null=True)
    updated_at = IntegerField()

    class Meta:
        db_table = 'computed_review_rating'


class Rating(BaseModel):
    company = ForeignKeyField(db_column='company_id', rel_model=Company)
    created_at = IntegerField()
    group = CharField()
    value = FloatField()

    class Meta:
        db_table = 'rating'
