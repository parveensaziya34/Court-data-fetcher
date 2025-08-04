import sqlite3
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                filing_year TEXT,
                captcha_used TEXT,
                raw_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    init_db()
    
def log_query(case_type, case_number, filing_year, captcha_used, raw_response):
    db = get_db()
    db.execute(
        'INSERT INTO queries (case_type, case_number, filing_year, captcha_used, raw_response) '
        'VALUES (?, ?, ?, ?, ?)',
        (case_type, case_number, filing_year, captcha_used, raw_response)
    )
    db.commit()