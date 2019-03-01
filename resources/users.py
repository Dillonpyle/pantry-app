import json

from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal,
                           marshal_with, url_for)

from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import models

from flask_cors import CORS

user_fields = {
    'id': fields.String,
    'username': fields.String,
}


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        super().__init__()

    # get all users
    def get(self):
        users = [marshal(user, user_fields) for user in models.User.select()]
        return {'users': users}

    # register users
    def post(self):
        args = self.reqparse.parse_args()
        if args['password']:
            print(args, ' this is args')
            user = models.User.create_user(**args)
            login_user(user)

            return marshal(user, user_fields,), 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)


class UserLogin(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help="No Username Provided",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help="No Password Provided",
            location=['form', 'json']
        )
        super().__init__()

    # Get route for user login
    def post(self):
        args = self.reqparse.parse_args()
        print("Arguments from UserLogin class", args)
        try:
            user = models.User.get(
                models.User.username == args['username'])
        except models.User.DoesNotExist:
            return make_response(
                json.dumps({
                    "error": "User does not exist in the database. Please register an account instead."
                }), 400
            )
        else:
            # Need to check if the right password was entered
            if check_password_hash(user.password, args['password']):
                # Login the user
                login_user(user)
                print("User found in database: ", user.username)
                return make_response(json.dumps({
                    "id": user.id,
                    "username": user.username
                }), 200)
            else:
                return make_response(
                    json.dumps({
                        "error": "User password was incorrectly entered. Please enter the correct password."
                    }), 400
                )


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
api.add_resource(
    UserLogin,
    '/login',
    endpoint='login')
