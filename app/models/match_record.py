from datetime import datetime
from app.extensions import db

class MatchRecord(db.Model):
    __tablename__ = 'match_records'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    loser_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, room_id, winner_id, loser_id):
        record = cls(room_id=room_id, winner_id=winner_id, loser_id=loser_id)
        db.session.add(record)
        db.session.commit()
        return record

    @classmethod
    def get_by_room(cls, room_id):
        return cls.query.filter_by(room_id=room_id).first()
