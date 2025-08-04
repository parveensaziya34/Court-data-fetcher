from app import db
from datetime import datetime

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50), nullable=False)
    case_number = db.Column(db.String(50), nullable=False)
    filing_year = db.Column(db.String(4), nullable=False)
    captcha_used = db.Column(db.String(10), nullable=False)
    raw_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Query {self.case_type}/{self.case_number}/{self.filing_year}>'