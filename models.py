import datetime

from peewee import *
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user


import config
DATABASE = SqliteDatabase('projectdatabase.sqlite')


class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique=True)
    password = CharField()
    description = TextField() # 				Playstyle, About section
    apex = TextField()
    apex_platform = TextField()
    overwatch = TextField()
    overwatch_platform = TextField()
    fortnite = TextField()
    fortnite_platform = TextField()



    # rating = IntegerField()

    class Meta:
        database = DATABASE

    def get_stream(self):
        return Review.select().where(
            (Review.user == self)
            )

    @classmethod
    def create_user(cls, username, email, password, description, apex, apex_platform, overwatch, overwatch_platform, fortnite, fortnite_platform):
        email = email.lower()

        try:
            user = cls.select().where(
            (cls.email == email)
            ).get()
            
            return False
        except cls.DoesNotExist:
            user = cls(username=username, email=email, description=description, apex=apex, apex_platform=apex_platform, overwatch=overwatch, overwatch_platform=overwatch_platform, fortnite=fortnite, fortnite_platform=fortnite_platform)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            return user




class Review(Model):	
    user = ForeignKeyField(model=User, related_name='review_set', backref='reviews', null=True)	# id of the person that the review is about
    username = CharField() 																		# the person that wrote the review
    created_at = DateTimeField(default=datetime.datetime.now)
    description = TextField()
    rating = IntegerField()




    @classmethod
    def create_review(cls, user, username, description, rating): # user is user id, must be sent from client

        review = cls(user=user, username=username, description=description, rating=rating)
        review.save()
        return review



    class Meta:
        database = DATABASE
        order_By = ('-created_at')



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Review], safe=True)
    DATABASE.close()