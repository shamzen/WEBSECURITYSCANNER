AI Web Security Scanner

Overview

This is an AI-powered web security scanner that detects vulnerabilities such as SQL Injection (SQLi), Cross-Site Scripting (XSS), CSRF, and security misconfigurations. It is built using Flask (Python) for the backend and a simple HTML, CSS, and JavaScript frontend.

Features

✅ Detects common vulnerabilities:

SQL Injection (SQLi)

Cross-Site Scripting (XSS)

CSRF (Cross-Site Request Forgery)

Security Misconfigurations

✅ Stores results in a database (SQLite/PostgreSQL)
✅ User-friendly web interface
✅ Fast and efficient scanning

Installation Guide

Step 1: Clone the Repository

git clone https://github.com/your-repo/AI_Web_Scanner.git
cd AI_Web_Scanner

Step 2: Create a Virtual Environment

python -m venv venv

Activate on Windows:

venv\Scripts\activate

Activate on Linux/macOS:

source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Run the Application

python app.py

Open http://127.0.0.1:5000/ in your browser.

Usage

Enter a URL in the input field.

Click the Scan button.

View vulnerability results with severity levels.

Folder Structure

AI_Web_Scanner/
│-- templates/
│   ├── index.html      # Frontend UI
│-- static/             # Static files (CSS, JS)
│-- app.py              # Flask application
│-- scanner.py          # Vulnerability detection logic
│-- requirements.txt     # Dependencies
│-- README.md           # Documentation

API Endpoints

Method

Endpoint

Description

POST

/scan

Scans a given URL for vulnerabilities

Example cURL request:

curl -X POST http://127.0.0.1:5000/scan -d "url=http://test.com"

Contributing

Fork the repo and create a new branch.

Make your changes and test them.

Submit a pull request with a detailed description.

License

This project is open-source under the MIT License.

🚀 Developed by Sham | Ethical Hacker & Security Researcher 🔥