import json
from datetime import datetime

LOG_FILE = "audit_log.json"

def log_query(query, is_safe, security_msg, answer=None):
    """Log every query with timestamp"""
    
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "security_passed": is_safe,
        "security_message": security_msg,
        "answer_given": answer[:100] if answer else None,
        "blocked": not is_safe
    }
    
    # Load existing logs
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except:
        logs = []
    
    # Add new log
    logs.append(log_entry)
    
    # Save back
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return log_entry

def get_all_logs():
    """Get all audit logs"""
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except:
        return []