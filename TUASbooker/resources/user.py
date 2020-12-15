from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from schemas.user import UserSchema

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.user import User
from models.bookings import Booking

from schemas.booking import BookingSchema
from schemas.user import UserSchema

from utils import hash_password

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=("email", ))
booking_list_schema = BookingSchema(many=True)

class UserBookingListResource(Resource):
    @jwt_optional
    @use_kwargs({"visibility": fields.Str(missing="public")})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
        bookings = Booking.get_all_by_user(user_id=user.id, visibility=visibility)
        return booking_list_schema.dump(bookings).data, HTTPStatus.OK

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)
        if errors:
            return{"message": "Validation error", "errors": errors}, HTTPStatus.BAD_REQUEST

        username = json_data.get("username")
        email = json_data.get("email")
        non_hash_password = json_data.get("password")

        if User.get_by_username(data.get("username")):
            return {"message": "username already used"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get("email")):
            return {"message": "email already used"}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        user = User(**data)

        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK

    @jwt_required
    def delete(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            user.delete()
        else:
            return {"message": "you do not have permission to delete this user"}, HTTPStatus.BAD_REQUEST

        return {"message": "user deleted"}, HTTPStatus.OK


class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user).data, HTTPStatus.OK

    @jwt_required
    def patch(self):
        json_data = request.get_json()
        user = User.get_by_id(id=get_jwt_identity())

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        user.username = json_data.get('username') or user.username
        user.email = json_data.get('email') or user.email
        user.password = hash_password(json_data.get('password')) or user.password

        user.save()
        return user_schema.dump(user).data, HTTPStatus.OK