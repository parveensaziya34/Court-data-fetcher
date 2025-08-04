from flask import Blueprint, render_template, request, current_app
from app.scraper import get_captcha_and_state, submit_case_details, parse_case_details
from app.database import log_query
from app.utils import cache_session, get_session
import base64
import uuid

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/fetch', methods=['POST'])
def fetch():
    case_type = request.form['case_type']
    case_number = request.form['case_number']
    filing_year = request.form['filing_year']
    
    try:
        # Get CAPTCHA and initial state
        captcha_image, state, session = get_captcha_and_state()
        # Generate unique token
        token = str(uuid.uuid4())
        # Store in cache
        cache_session(token, {
            'session': session,
            'case_type': case_type,
            'case_number': case_number,
            'filing_year': filing_year,
            'state': state
        })
        return render_template(
            'captcha.html',
            captcha_image=base64.b64encode(captcha_image).decode('utf-8'),
            token=token
        )
    except Exception as e:
        import traceback
        error_details = f"{str(e)}\n{traceback.format_exc()}"
        current_app.logger.error(f"CAPTCHA fetch failed: {error_details}")
        # Show the error details on the error page for debugging
        return render_template('error.html', message=f"Court service unavailable. Error: {str(e)}")

@bp.route('/results', methods=['POST'])
def results():
    token = request.form['token']
    captcha_text = request.form['captcha_text']
    
    # Retrieve from cache
    cache_data = get_session(token)
    if not cache_data:
        return render_template('error.html', message="Session expired. Please start over.")
    
    try:
        # Submit case details with CAPTCHA
        html_response = submit_case_details(
            cache_data['session'],
            cache_data['state'],
            cache_data['case_type'],
            cache_data['case_number'],
            cache_data['filing_year'],
            captcha_text
        )
        
        # Parse response
        case_details, pdf_links = parse_case_details(html_response)
        
        # Log to database
        log_query(
            case_type=cache_data['case_type'],
            case_number=cache_data['case_number'],
            filing_year=cache_data['filing_year'],
            captcha_used=captcha_text,
            raw_response=html_response
        )
        
        return render_template(
            'results.html',
            details=case_details,
            pdf_links=pdf_links,
            recent_order=pdf_links[0] if pdf_links else None
        )
        
    except Exception as e:
        current_app.logger.error(f"Case fetch failed: {str(e)}")
        return render_template('error.html', message="Invalid case details or CAPTCHA. Please verify and try again.")