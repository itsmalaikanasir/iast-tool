import requests
import re
import time

def run_iast_scan(target_url):
    findings = []

    # ---- SQL Injection heuristic ----
    payload = "' OR '1'='1"
    try:
        r = requests.get(target_url, params={"id": payload}, timeout=5)
        if re.search(r"sql|syntax|mysql|postgres", r.text, re.I):
            findings.append({
                "severity": "High",
                "type": "SQL Injection",
                "endpoint": target_url,
                "description": "Possible SQL injection via unsanitized parameter",
                "recommendation": "Use parameterized queries (prepared statements)"
            })
    except:
        pass

    # ---- XSS heuristic ----
    xss_payload = "<script>alert(1)</script>"
    try:
        r = requests.get(target_url, params={"q": xss_payload}, timeout=5)
        if xss_payload in r.text:
            findings.append({
                "severity": "Medium",
                "type": "Cross-Site Scripting (XSS)",
                "endpoint": target_url,
                "description": "Reflected XSS detected",
                "recommendation": "Escape user input before rendering"
            })
    except:
        pass

    # ---- Insecure Headers ----
    try:
        r = requests.get(target_url, timeout=5)
        headers = r.headers

        if "Content-Security-Policy" not in headers:
            findings.append({
                "severity": "Low",
                "type": "Missing Security Headers",
                "endpoint": target_url,
                "description": "CSP header is missing",
                "recommendation": "Add Content-Security-Policy header"
            })
    except:
        pass

    # ---- Simulated Runtime Delay (IAST behavior) ----
    time.sleep(1)

    return findings
