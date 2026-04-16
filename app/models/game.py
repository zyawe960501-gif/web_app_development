from datetime import datetime
from app.models import db

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.String(20), default='waiting', nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    creator = db.relationship('User', foreign_keys=[created_by])

    @classmethod
    def create(cls, name, created_by, is_private=False):
        new_room = cls(name=name, created_by=created_by, is_private=is_private)
        db.session.add(new_room)
        db.session.commit()
        return new_room

    @classmethod
    def get_by_id(cls, room_id):
        return cls.query.get(room_id)

    @classmethod
    def get_all_waiting_public(cls):
        return cls.query.filter_by(status='waiting', is_private=False).all()

    @classmethod
    def update_status(cls, room_id, new_status):
        room = cls.get_by_id(room_id)
        if room:
            room.status = new_status
            db.session.commit()
        return room


class MatchRecord(db.Model):
    __tablename__ = 'match_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opponent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    result = db.Column(db.String(20), nullable=False)
    score_change = db.Column(db.Integer, default=0, nullable=False)
    played_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    player = db.relationship('User', foreign_keys=[player_id])
    opponent = db.relationship('User', foreign_keys=[opponent_id])
    room = db.relationship('Room', foreign_keys=[room_id])

    @classmethod
    def create(cls, room_id, player_id, opponent_id, result, score_change):
        new_record = cls(
            room_id=room_id, 
            player_id=player_id, 
            opponent_id=opponent_id, 
            result=result, 
            score_change=score_change
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @classmethod
    def get_by_player_id(cls, player_id):
        return cls.query.filter_by(player_id=player_id).order_by(cls.played_at.desc()).all()
