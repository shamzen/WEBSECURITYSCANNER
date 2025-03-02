from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# SQL Injection Test
def detect_sqli(url):
    payloads = ["' OR '1'='1 --", "\" OR \"1\"=\"1 --","' UNION SELECT NULL,NULL --"]
    for payload in payloads:
        test_url = url + payload if "?" in url else url + "/'"
        try:
            response = requests.get(test_url, timeout=5, verify=False)
            error_keywords = ["syntax error", "mysql", "sql syntax", "database error", "You have an error in your SQL"]
            if any(keyword in response.text.lower() for keyword in error_keywords):
                return True
        except requests.exceptions.RequestException:
            pass
    return False

# XSS Test
def detect_xss(url):
    payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
    for payload in payloads:
        test_url = url + payload if "?" in url else url + "/<script>alert('XSS')</script>"
        try:
            response = requests.get(test_url, timeout=5, verify=False)
            if payload in response.text:
                return True
        except requests.exceptions.RequestException:
            pass
    return False

# Subdomain Finder (Fixed)
def find_subdomains(domain):
    crt_url = f"https://crt.sh/?q={domain}&output=json"
    subdomains = set()
    try:
        response = requests.get(crt_url, timeout=10, verify=False)
        if response.status_code == 200:
            try:
                json_data = response.json()
                for entry in json_data:
                    if "name_value" in entry:
                        subdomains.update(entry["name_value"].split("\n"))  # Handle multiple subdomains per entry
            except ValueError:
                return ["Error: Invalid JSON response"]
        else:
            return [f"Error: HTTP {response.status_code}"]
    except requests.exceptions.RequestException as e:
        return [f"Error: {str(e)}"]
    return list(subdomains)

# Open Redirect Check
def detect_open_redirect(url):
    payload = "http://evil.com"
    test_url = f"{url}?next={payload}"
    try:
        response = requests.get(test_url, timeout=5, verify=False, allow_redirects=False)
        if response.status_code in [301, 302] and payload in response.headers.get("Location", ""):
            return True
    except requests.exceptions.RequestException:
        pass
    return False

# Clickjacking Check (X-Frame-Options)
def detect_clickjacking(url):
    try:
        response = requests.get(url, timeout=5, verify=False)
        if "X-Frame-Options" not in response.headers:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

# CORS Misconfiguration Check
def detect_cors_misconfig(url):
    try:
        response = requests.get(url, timeout=5, verify=False)
        if "Access-Control-Allow-Origin" in response.headers and "*" in response.headers["Access-Control-Allow-Origin"]:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

# CSRF Detection (Basic Check)
def detect_csrf(url):
    try:
        response = requests.get(url, timeout=5, verify=False)
        if "csrf" not in response.text.lower():
            return True  # If there is no CSRF token in the page, it's vulnerable
    except requests.exceptions.RequestException:
        pass
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    domain = url.replace("http://", "").replace("https://", "").split('/')[0]

    result = {
        "url": url,
        "sql_injection": detect_sqli(url),
        "xss": detect_xss(url),
        "subdomains": find_subdomains(domain),
        "open_redirect": detect_open_redirect(url),
        "clickjacking": detect_clickjacking(url),
        "cors_misconfig": detect_cors_misconfig(url),
        "csrf_vulnerable": detect_csrf(url)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
