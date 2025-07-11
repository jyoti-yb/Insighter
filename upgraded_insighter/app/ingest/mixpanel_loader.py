import pandas as pd
from app.db.session import SessionLocal
from app.db.models import User, Event
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def load_mixpanel_json(json_file_path):
    session = SessionLocal()
    data = pd.read_json(json_file_path)

    for _, row in data.iterrows():
        anon_id = row.get('distinct_id')
        timestamp = row.get('time')
        event_name = row.get('event')
        properties = row.get('properties', {})

        # Create user if not exists
        user = session.query(User).filter_by(anonymous_id=anon_id).first()
        if not user:
            user = User(anonymous_id=anon_id)
            session.add(user)
            session.flush()  # get user.id

        # Add event
        event = Event(
            user_id=user.id,
            event_name=event_name,
            timestamp=datetime.fromtimestamp(timestamp / 1000),
            properties=properties
        )
        session.add(event)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.close()
