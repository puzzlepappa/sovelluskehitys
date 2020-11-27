from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


def validate_duration(n):
    if n < 1:
        raise ValidationError('Duration must be greater than 0. ')
    if n > 24:
        raise ValidationError('Duration cannot be over 24')

class RoomSchema(Schema):
    class Meta:
        ordered = True

    room_id = fields.Integer(dump_only=True)
    room_name = fields.String(required=True, validate=[validate.Length(max=100)])
    room_description = fields.String(validate=[validate.Length(max=200)])
    room_reserve_duration = fields.Integer(validate=validate_duration)
    room_is_public = fields.Boolean(dump_only=True)
    author = fields.Nested(UserSchema, attribute="user", dump_only=True, only=["id", "username"])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

