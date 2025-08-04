import os
import sqlite3
import requests
import uuid
import base64
import threading
import time
from flask import Flask, render_template, request, g, url_for, session, flash, redirect
from bs4 import BeautifulSoup
from App.database import log_query, init_db, get_db
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DATABASE'] = 'court_data.db'

# Database setup
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with app.app_context():
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

# Session cache
session_cache = {}
cache_lock = threading.Lock()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    try:
        # Get form data
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number')
        filing_year = request.form.get('filing_year')

        # Validate
        if not all([case_type, case_number, filing_year]):
            flash("All fields are required!", "danger")
            return redirect(url_for('index'))

        # Simulate fetch from court website or database (replace with actual fetch logic)
        # Example mock result
        result = {
            "case_type": case_type,
            "case_number": case_number,
            "filing_year": filing_year,
            "status": "Pending",
            "last_hearing": "2025-07-15",
            "next_hearing": "2025-08-10",
            "judge": "Justice A. B. Sharma"
        }

        # Convert result to JSON for logging
        raw_response = json.dumps(result)

        # Log in DB
        log_query(case_type, case_number, filing_year, captcha_used=False, raw_response=raw_response)

        # Pass data to results page
        session['case_details'] = result  # Or use redirect with query params or temporary storage
        return redirect(url_for('results'))

    except Exception as e:
        print(f"Error: {e}")
        flash("An unexpected error occurred. Please try again.", "danger")
        return render_template('error.html')

@app.route('/results')
def results():
    case_details = session.get('case_details')
    if not case_details:
        flash("No case data found. Please search again.", "warning")
        return redirect(url_for('index'))

    return render_template('results.html', details=case_details)

app.route('/captcha', methods=['POST'])
def results():
    return render_template('captcha.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)