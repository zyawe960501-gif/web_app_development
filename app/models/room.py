from datetime import datetime
from app.extensions import db

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_code = db.Column(db.String(10), unique=True, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(20), default='waiting')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, room_code, host_id):
        new_room = cls(room_code=room_code, host_id=host_id, status='waiting')
        db.session.add(new_room)
        db.session.commit()
        return new_room

    @classmethod
    def get_by_code(cls, room_code):
        return cls.query.filter_by(room_code=room_code).first()
        
    @classmethod
    def get_by_id(cls, room_id):
        return cls.query.get(room_id)

    @classmethod
    def join_room(cls, room_code, guest_id):
        room = cls.get_by_code(room_code)
        if room and room.status == 'waiting' and room.guest_id is None:
            room.guest_id = guest_id
            room.status = 'playing'
            db.session.commit()
            return room
        return None

    @classmethod
    def update_status(cls, room_id, status):
        room = cls.query.get(room_id)
        if room:
            room.status = status
            db.session.commit()
            return room
        return None
