import os
from unittest import TestCase
from models import db, connect_db, User

os.environ['DATABASE_URL'] = "postgresql:///healthy_spoon_test"

from app import app

db.create_all()

def delete_all_from_model(model_name):
    """Clear database"""
    results = model_name.query.all()
    for result in results:
        db.session.delete(result)
    db.session.commit()

# Create test database tables
db.create_all()

# Disable WTForms use of CSRF during testing.
app.config['WTF_CSRF_ENABLED'] = False
