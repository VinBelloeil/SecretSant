from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    created = db.Column(db.DateTime, default = datetime.now)

    exclusions = db.relationship(
        'Exclusion',
        foreign_keys='Exclusion.participant_id',
        back_populates='participant',
        cascade='all, delete-orphan')
    
    assignments_given = db.relationship(
        'Assignment',
        foreign_keys='Assignment.giver_id',
        back_populates='giver',
        cascade='all, delete-orphan')


class Exclusion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    excluded_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)

    participant = db.relationship('Participant', foreign_keys=[participant_id], back_populates='exclusions')
    excluded = db.relationship('Participant', foreign_keys=[excluded_id])


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    draw_id = db.Column(db.Integer, db.ForeignKey('draw.id'), nullable = False)
    giver_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)

    draw = db.relationship('Draw', foreign_keys=[draw_id], back_populates='assignments')
    giver = db.relationship('Participant', foreign_keys=[giver_id], back_populates='assignments_given')
    receiver = db.relationship('Participant', foreign_keys=[receiver_id])


class Draw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default = datetime.now)

    assignments = db.relationship('Assignment', back_populates='draw', cascade='all, delete-orphan')
