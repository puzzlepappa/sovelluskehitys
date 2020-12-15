from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.bookings import Booking, bookings_list
from models.rooms import Room
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.booking import BookingSchema
import datetime

booking_schema = BookingSchema()
booking_list_schema = BookingSchema(many=True)

class BookingListResource(Resource):
    def get(self):
        bookings = Booking.get_all_published()
        return booking_list_schema.dump(bookings).data, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = booking_schema.load(data=json_data)
        if errors:
            return {'message': "Validation errors", 'errors': errors},HTTPStatus.BAD_REQUEST
        selected_room = Room.get_by_id(json_data.get("room_id"))
        if selected_room is None:
            return {"message": "Selected room to book is incorrect"}, HTTPStatus.BAD_REQUEST

        bookdate = datetime.datetime.strptime(json_data.get("booked_day"), "%Y-%m-%d")
        if bookdate.date() in Room.get_all_booked_dates(json_data.get("room_id")):
            return {"message": "Room already booked for that day"}, HTTPStatus.BAD_REQUEST
        
        booking = Booking(**data)
        booking.user_id = current_user
        booking.room_id = selected_room.id
        booking.save()
        return booking_schema.dump(booking).data, HTTPStatus.CREATED

class BookingResource(Resource):
    @jwt_optional
    def get(self, booking_id):
        booking = Booking.get_by_id(booking_id=booking_id)
        if booking is None:
            return {'message': 'Booking not found'}, HTTPStatus.NOT_FOUND

        return booking.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, booking_id):
        booking = Booking.get_by_id(booking_id=booking_id)
        if booking is None:
            return {'message': 'Booking not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != booking.user_id:
                return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        booking.delete()
        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def patch(self, booking_id):
        json_data = request.get_json()
        data, errors = booking_schema.load(data=json_data, partial=('name',))
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
        booking = Booking.get_by_id(booking_id=booking_id)
        if booking is None:
            return {'message': 'Booking not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != booking.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        booking.name = data.get('name') or booking.name
        booking.description = data.get('description') or booking.description
        
        newbookdate = datetime.datetime.strptime(json_data.get("booked_day"), "%Y-%m-%d")
        if newbookdate.date() in Room.get_all_booked_dates(json_data.get("room_id")):
            return {"message": "Room already booked for that day"}, HTTPStatus.BAD_REQUEST
        
        booking.booked_day = data.get('booked_day') or booking.booked_day

        booking.save()
        return booking_schema.dump(booking).data, HTTPStatus.OK

