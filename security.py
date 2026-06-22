# Security Guardrails - This makes your project UNIQUE

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "forget your instructions",
    "you are now",
    "act as",
    "pretend you are",
    "disregard",
    "override",
    "jailbreak",
    "bypass"
]

TOXIC_PATTERNS = [
    "hack", "exploit", "steal",
    "illegal", "weapon", "bomb"
]

def check_prompt_injection(query):
    """Detect prompt injection attacks"""
    query_lower = query.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in query_lower:
            return True, f"Prompt injection detected: '{pattern}'"
    return False, None

def check_toxic_content(query):
    """Detect harmful content"""
    query_lower = query.lower()
    for pattern in TOXIC_PATTERNS:
        if pattern in query_lower:
            return True, f"Harmful content detected"
    return False, None

def check_query_length(query):
    """Prevent extremely long queries"""
    if len(query) > 1000:
        return True, "Query too long (max 1000 characters)"
    return False, None

def run_security_checks(query):
    """Run ALL security checks — returns (is_safe, message)"""
    
    # Check 1: Prompt Injection
    flagged, msg = check_prompt_injection(query)
    if flagged:
        return False, f"🚨 Security Alert: {msg}"
    
    # Check 2: Toxic Content
    flagged, msg = check_toxic_content(query)
    if flagged:
        return False, f"🚨 Security Alert: {msg}"
    
    # Check 3: Length Check
    flagged, msg = check_query_length(query)
    if flagged:
        return False, f"🚨 Security Alert: {msg}"
    
    return True, "✅ Query passed all security checks"