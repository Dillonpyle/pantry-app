import json

from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal,
                           marshal_with, url_for)

from flask_login import login_user, logout_user, login_required, current_user
import models

user_fields = {
    'username': fields.String,
    'id': fields.Integer
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


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
