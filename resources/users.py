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
    'apex': fields.String, 
    'apex_platform': fields.String,
    'overwatch': fields.String,
    'overwatch_platform': fields.String,
    'fortnite': fields.String,
    'fortnite_platform': fields.String

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
            'apex',
            required=True,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'apex_platform',
            required=True,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'overwatch',
            required=True,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'overwatch_platform',
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


        super().__init__()

        

    def get(self):
        users = [marshal(user, user_fields) for user in models.User.select()]
        return {"users" : users}, 200


    # register
    def post(self): 
        print('called?')
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
            'apex',
            required=False,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'apex_platform',
            required=False,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'overwatch',
            required=False,
            help='description entered?',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'overwatch_platform',
            required=False,
            help='description entered?',
            location=['form', 'json']
            )
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

    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(**args).where(models.User.id==id)
        query.execute()
        return (models.User.get(models.User.id==id), 200)





    # edit profile, complete profile,


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

