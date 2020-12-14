from extensions import db

bookings_list = []


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    booked_day = db.Column(db.Date(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default = db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default = db.func.now(), onupdate = db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    room_id = db.Column(db.Integer(), db.ForeignKey("rooms.id"), nullable=False)

    @classmethod
    def get_all_published(cls):
        return cls.query.all()

    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):
        if visibility == 'public':
            return cls.query.filter_by(user_id=user_id, is_publish=True).all()
        elif visibility == 'private':
            return cls.query.filter_by(user_id=user_id, is_publish=False).all()
        else:
            return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_id(cls, booking_id):
        return cls.query.filter_by(id=booking_id).first()

    @classmethod
    def get_all_booked_dates(cls, room_id):
        return cls.query.filter_by(room_id=room_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



