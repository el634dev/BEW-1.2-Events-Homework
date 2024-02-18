"""Create database models to represent tables."""
from events_app import db
from sqlalchemy.orm import backref
from sqlalchemy import Column, DateTime, Integer, String

# Create a model called `Guest` with the following fields:
class Guest(db.Model):
    """Guest Model"""
    # - id: primary key
    id = db.Column(db.Integer, primary_key=True)
    # - name: String column
    name = db.Column(db.String(80), nullable=False)
    # - email: String column
    email = db.Column(db.String(80), nullable=False)
    # - phone: String column
    phone = db.Column(db.String(80), nullable=False)
    # - events_attending: relationship to "Event" table with a secondary table
    events_attending = db.relationship('Event', secondary='guest_event', backref='guests')

# -----------------------------------
# Create a model called `Event` with the following fields:
class Event(db.Model):
    """Event Model"""
    # - id: primary key
    id = db.Column(db.Integer, primary_key=True)
    # - title: String column
    title = db.Column(db.String(40), nullable=False)
    # - description: String column  
    description = db.Column(db.String(80), nullable=False)
    # - date_and_time: DateTime column
    date_and_time = db.Column(db.DateTime, nullable=False)
    # - guests: relationship to "Guest" table with a secondary table
    guest = db.relationship("Guest", secondary="guest_event")

# STRETCH CHALLENGE: Add a field `event_type` as an Enum column that denotes the
# type of event (Party, Study, Networking, etc)

# Create a table `guest_event_table` with the following columns:
guest_event_table = db.Table('guest_event',
        # - event_id: Integer column (foreign key)
        db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
        # - guest_id: Integer column (foreign key)
        db.Column('guest_id', db.Integer, db.ForeignKey('guest.id'))
)
