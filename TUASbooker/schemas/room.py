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

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    reserve_duration = fields.Integer(validate=validate_duration)
    author = fields.Nested(UserSchema, attribute="user", dump_only=True, only=["id", "username"])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

