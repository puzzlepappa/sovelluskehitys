from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.rooms import rooms_list, Room
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.room import RoomSchema

room_schema = RoomSchema()
Room_list_schema = RoomSchema(many=True)

class RoomListResrouce(Resource):
    def get(self):
        rooms = Room.get_all_published()
        return Room_list_schema.dump(rooms).data, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = room_schema.load(data=json_data)
        if errors:
            return {'message': "Validation errors", 'errors': errors},HTTPStatus.BAD_REQUEST

        room = Room(**data)
        room.user_id = current_user
        room.save()
        return room_schema.dump(room).data, HTTPStatus.CREATED
class RoomResource(Resource):
    @jwt_optional
    def get(self, room_id):
        room = Room.get_by_id(room_id=room_id)
        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if room.is_public == False and room.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return room.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, room_id):
        room = Room.get_by_id(room_id=room_id)
        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != room.user_id:
                return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        room.delete()
        return {}, HTTPStatus.NO_CONTENT


    @jwt_required
    def patch(self, room_id):
        json_data = request.get_json()
        data, errors = room_schema.load(data=json_data, partial=('name',))
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
        room = Room.get_by_id(room_id=room_id)
        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != room.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        room.name = data.get('name') or room.name
        room.description = data.get('description') or room.description

        room.save()
        return room_schema.dump(room).data, HTTPStatus.OK

class RoomPublishResource(Resource):
    def put(self, room_id):
        room = Room.get_by_id(room_id=room_id)
        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND
        room.is_public = True
        room.save()
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, room_id):
        room = Room.get_by_id(room_id=room_id)
        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND
        room.is_public = False
        room.save()
        return {}, HTTPStatus.NO_CONTENT