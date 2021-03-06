import json
from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import check_password_hash


import models

user_fields = {
    'id' : fields.Integer,
    'username' : fields.String,
    'email': fields.String,
    'description': fields.String,
    'fortnite': fields.String,
    'fortnite_platform': fields.String,
    'rating': fields.Integer,
    'accountId': fields.String,

}

relationship_fields = {
    'owner_id': fields.String,
    'other_person': fields.String,
    'like': fields.Boolean, 
    'chatroom_id': fields.String,
}

chatroom_fields = {
    'chatroom_id': fields.String, 
    'message': fields.String,
    'sender': fields.String, 
    'receiver': fields.String

}

def user_or_404(id):
    try:
        user = models.User.get(models.User.id == id)
    except models.User.DoesNotExist:
        abort(404)
    else:
        return user

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='no username provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='no email provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='no password provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'description',
            required=True,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'fortnite',
            required=True,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'fortnite_platform',
            required=True,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'accountId',
            required=True,
            help='missing accountId',
            location=['form', 'json']
            )


        super().__init__()

        
        # get all users 
    def get(self):
        users = [marshal(user, user_fields) for user in models.User.select().where((models.User.email != ""))]
        return {"users" : users}, 200


    # register
    def post(self): 
        args = self.reqparse.parse_args()
        user = models.User.create_user(**args)
        if user: 
            return marshal(user, user_fields), 200
        else:
            return "This email is already taken.", 201

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'fortnite',
            required=False,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'fortnite_platform',
            required=False,
            help='description entered?',
            location=['form', 'json']
            )
        super().__init__()


    # get all users that isn't yourself
    def get(self, id): 
        users = [marshal(user, user_fields) for user in models.User.select().where((models.User.id != id))]
        return users, 200


    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(**args).where(models.User.id==id)
        query.execute()
        return (models.User.get(models.User.id==id), 200)


class RelationshipList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
        'owner_id',
        required=True,
        help='no ownerid entered?',
        location=['form', 'json']
        )
        self.reqparse.add_argument(
        'other_person',
        required=True,
        help='other person entered?',
        location=['form', 'json']
        )
        self.reqparse.add_argument(
        'like',
        required=True,
        help='like not entered?',
        location=['form', 'json']
        )
        self.reqparse.add_argument(
        'chatroom_id',
        required=True,
        help='chatroom not entered?',
        location=['form', 'json']
        )
        super().__init__()


    def get(self): 
        # gets all relationships in database 
        relationships = [marshal(relationship, relationship_fields) for relationship in models.Relationship.select()]
        return relationships


        # create new relationship
    def post(self):
        args = self.reqparse.parse_args()
        relationship = models.Relationship.create_relationship(**args)
        return marshal(relationship, relationship_fields) # returns the newly created relation




class Relationship(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
        'owner_id',
        required=False,
        help='no ownerid entered?',
        location=['form', 'json']
        )
        self.reqparse.add_argument(
        'other_person',
        required=False,
        help='other person entered?',
        location=['form', 'json']
        )
        self.reqparse.add_argument(
        'like',
        required=False,
        help='like not entered?',
        location=['form', 'json']
        )
        self.reqparse.add_argument(
        'chatroom_id',
        required=True,
        help='chatroom not entered?',
        location=['form', 'json']
        )
        super().__init__()

    def get(self, id):
        # args = self.reqparse.parse_args()
        relationships = [marshal(relationship, relationship_fields) for relationship in models.Relationship.select().where((models.Relationship.owner_id == id))]
        return relationships
        # get back all the relationships for this id 

    def post(self, id): 
        args = self.reqparse.parse_args()
        try: 

        # first = [marshal(item, relationship_fields)  for item in models.Relationship.select().where((models.Relationship.owner_id == args["other_person"]))]
        # second = [marshal(item, relationship_fields)  for item in first.select().where((models.Relationship.other_person == id))]
            user = models.Relationship.get( (models.Relationship.like == args["like"]) and (models.Relationship.owner_id == args["other_person"]) and (models.Relationship.other_person == id) )
        except models.DoesNotExist:
            return "Not Found"
        else: 
            return "Found" #marshal(user, relationship_fields)

class Login(Resource): 
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required = True,
            help = 'no username entered',
            location = ['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required = True,
            help = 'no password entered',
            location = ['form', 'json']
        )

        super().__init__()


    #login 

    def post(self):
        args = self.reqparse.parse_args()
        try:
            user = models.User.get(models.User.email == args["email"])
        except models.DoesNotExist: 
            return "Email/Password Incorrect"
        else:
            if check_password_hash(user.password, args["password"]):
                login_user(user)
                return marshal(user,user_fields), 200
            else:
                return "Email/Password Incorrect"

    #logout
    def delete(self):
        logout_user()
        return "Logout Successful", 200


class Chatroom(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'chatroom_id',
            required = True,
            help = 'no username entered',
            location = ['form', 'json']
        )
        self.reqparse.add_argument(
            'message',
            required = True,
            help = 'no password entered',
            location = ['form', 'json']
        )
        self.reqparse.add_argument(
            'sender',
            required = True,
            help = 'no password entered',
            location = ['form', 'json']
        )
        self.reqparse.add_argument(
            'receiver',
            required = True,
            help = 'no password entered',
            location = ['form', 'json']
        )


        super().__init__()


        # id is chatroom_id 
    def get(self, id):
        messages = [marshal(msg, chatroom_fields) for msg in models.Chatroom.select().where((models.Chatroom.chatroom_id == id))]
        return messages

    def post(self, id):
        args = self.reqparse.parse_args()
        message = models.Chatroom.create_chatroom(**args)
        return marshal(message, chatroom_fields) # returns the newly created relation







users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
api.add_resource(
    User,
    '/users/<int:id>',
    endpoint='edit'
    )
api.add_resource(
    Login,
    '/users/login',
    endpoint='login'
)
api.add_resource(
    Relationship,
    '/users/relationship/<int:id>',
    endpoint='getrelations'
)
api.add_resource(
    RelationshipList,
    '/users/relationship',
    endpoint='createrelations'
)


api.add_resource(
    Chatroom,
    '/users/chat/<string:id>',
    endpoint='chatroom'
)

