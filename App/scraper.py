import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://delhihighcourt.nic.in/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': BASE_URL + 'case.asp'
}

def get_captcha_and_state():
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # Get initial page
    response = session.get(BASE_URL + 'case.asp', timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract state tokens
    state = {
        'viewstate': soup.find('input', {'name': '__VIEWSTATE'})['value'],
        'viewstategenerator': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
        'eventvalidation': soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
    }
    
    # Get CAPTCHA image
    captcha_response = session.get(BASE_URL + 'validate_num.asp', timeout=10)
    captcha_response.raise_for_status()
    
    return captcha_response.content, state, session

def submit_case_details(session, state, case_type, case_number, filing_year, captcha_text):
    data = {
        '__VIEWSTATE': state['viewstate'],
        '__VIEWSTATEGENERATOR': state['viewstategenerator'],
        '__EVENTVALIDATION': state['eventvalidation'],
        'txtcasedt': case_type,
        'txtcno': case_number,
        'txtyear': filing_year,
        'txtcode': captcha_text,
        'B1': 'Submit'
    }
    
    response = session.post(
        BASE_URL + 'case_status_2.asp',
        data=data,
        timeout=15
    )
    response.raise_for_status()
    
    return response.text

def parse_case_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    details = {}
    
    # Extract case metadata from tables
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].get_text(strip=True).rstrip(':')
                value = cells[1].get_text(strip=True)
                if key and value:
                    details[key] = value
    
    # Extract PDF links
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.lower().endswith('.pdf'):
            # Handle relative URLs
            if not href.startswith('http'):
                href = BASE_URL + href.lstrip('/')
            pdf_links.append({
                'title': link.get_text(strip=True) or 'Order PDF',
                'url': href
            })
    
    # Extract key fields explicitly
    case_info = {
        'Case Number': details.get('Case No'),
        'Filing Date': details.get('Filing Date'),
        'Next Hearing': details.get('Next Date'),
        'Petitioner': details.get('Petitioner'),
        'Respondent': details.get('Respondent'),
        'Judge': details.get('Judge'),
        'Status': details.get('Status')
    }
    
    return case_info, pdf_links