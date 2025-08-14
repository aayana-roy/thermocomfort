from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Mail configuration (replace with your SMTP server details)
app.config['MAIL_SERVER'] = 'smtp.example.com'  # e.g., 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com' # Optional, sets default sender

mail = Mail(app)