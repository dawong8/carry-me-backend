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
    fortnite = TextField()
    fortnite_platform = TextField()
    accountId = TextField()


    rating = IntegerField()

    class Meta:
        database = DATABASE

    def get_stream(self):
        return Review.select().where(
            (Review.user == self)
            )

    @classmethod
    def create_user(cls, username, email, password, description, fortnite, fortnite_platform, accountId):
        email = email.lower()

        try:
            user = cls.select().where(
            (cls.email == email)
            ).get()
            
            return False
        except cls.DoesNotExist:
            user = cls(username=username, email=email, description=description, fortnite=fortnite, fortnite_platform=fortnite_platform, accountId=accountId)
            user.password = generate_password_hash(password)
            user.rating = 50
            user.save()
            return user
        else:
            return user


class Relationship(Model):
	owner_id = TextField() #ForeignKeyField(model=User, related_name='relationship_set', backref='relationship', null=True)
	other_person = TextField()
	like = BooleanField() # true = like, false = pass


	class Meta: 
		database = DATABASE

	@classmethod
	def create_relationship(cls, owner_id, other_person, like):
		relation = cls(owner_id=owner_id, other_person=other_person, like=like)
		relation.save()
		return relation



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
    DATABASE.create_tables([User, Relationship, Review], safe=True)
    DATABASE.close()