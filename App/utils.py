import threading
import time
import uuid

# Session cache for CAPTCHA handling
session_cache = {}
cache_lock = threading.Lock()
SESSION_TIMEOUT = 300  # 5 minutes

def clean_cache():
    """Remove expired sessions"""
    current_time = time.time()
    with cache_lock:
        for token in list(session_cache.keys()):
            if current_time - session_cache[token]['timestamp'] > SESSION_TIMEOUT:
                del session_cache[token]

def cache_session(token, session_data):
    clean_cache()
    with cache_lock:
        session_data['timestamp'] = time.time()
        session_cache[token] = session_data

def get_session(token):
    clean_cache()
    with cache_lock:
        return session_cache.pop(token, None) if token else None