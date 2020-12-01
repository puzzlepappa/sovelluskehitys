from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema
from schemas.room import RoomSchema
import datetime


def validate_duration(n):
    if n < datetime.date.today():
        raise ValidationError('Cannot book room with dates from the past.')
    elif n.weekday() < 5:
        raise ValidationError('Cannot book rooms on weekends.')

class BookingSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    booked_day = fields.Date(required=True, validate=validate_duration)
    user_id = fields.Nested(UserSchema, attribute="user", dump_only=True, only=["id", "username"])
    room_id = fields.Nested(RoomSchema, attribute="rooms", dump_only=True, only=["id", "name"])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

