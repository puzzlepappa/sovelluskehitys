from extensions import db

rooms_list = []


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    is_public=db.Column(db.Boolean(),nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default = db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default = db.func.now(), onupdate = db.func.now())
    bookings = db.relationship('Booking', backref='rooms')

    @classmethod
    def get_all_public(cls):
        return cls.query.filter_by(room_is_public=True).all()

    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):
        if visibility == 'public':
            return cls.query.filter_by(author=user_id, room_is_public=True).all()
        elif visibility == 'private':
            return cls.query.filter_by(author=user_id, room_is_public=False).all()
        else:
            return cls.query.filter_by(author=user_id).all()

    @classmethod
    def get_by_id(cls, room_id):
        return cls.query.filter_by(id=room_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


