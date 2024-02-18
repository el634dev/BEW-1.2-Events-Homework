"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)


##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""
    # Get all events and send to the template
    events = Event.query.all()
    return render_template('index.html', events=events)

# --------------------------------------------
# Create a new event
@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html', 
                error='Incorrect datetime format! Please try again.')

        # Create a new event with the given title, description, &
        # datetime, then add and commit to the database
        new_event = Event(
            title = new_event_title,
            description = new_event_description,
            new_date = date_and_time
        )

        db.session.add(new_event)
        db.session.commit()
        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')

# ------------------------------
# Show a single event to the user
@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    # Get the event with the given id and send to the template
    single_event = Event.query.filter_by(id=event_id).first()
    return render_template('event_detail.html', single_event=single_event)

# ----------------------------------
@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    # Get the event with the given id from the database
    event_one = Event.query.filter_by(id=event_id).first()
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')

    if is_returning_guest:
        # Look up the guest by name. If the guest doesn't exist in the
        # database, render the event_detail.html template, and pass in an error
        # message as `error`.
        current_guest = Guest.query.filter_by(name=guest_name).one()

        if current_guest:
            current_guest.events_attending.append(event_one)
            db.session.commit()
            return render_template('event_detail.html', event_id=event_id)
        else:
            flash('Guest does not exist')
            return render_template(url_for('event_detail.html', event_id=event_id))
    else:
        # If the guest does exist, add the event to their
        # events_attending, then commit to the database.
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')

        # Create a new guest with the given name, email, and phone, and
        # add the event to their events_attending, then commit to the database.
        new_guest = Guest(
            name = guest_name,
            email = guest_email,
            phone = guest_phone,
            events_attending = event_one
        )

        new_guest.events_attending.append(event_one)
        db.session.add(new_guest)
        db.session.commit()

        flash('You have successfully RSVP\'d! See you there!')
        return redirect(url_for('main.event_detail', event_id=event_id))

# ------------------------------
@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    """Get the guest details"""
    # Get the guest with the given id and send to the template
    guest_one = Guest.query.filter_by(id=guest_id).first()
    return render_template('guest_detail.html', guest_one=guest_one)
