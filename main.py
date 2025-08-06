from flask import Flask, render_template, request, flash, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials

import os

GOOGLE_CREDENTIALS_ENV = os.environ.get('GOOGLE_CREDENTIALS')
CREDENTIALS_FILE = 'google-credentials.json'

if GOOGLE_CREDENTIALS_ENV and not os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(GOOGLE_CREDENTIALS_ENV)

app = Flask(__name__)
app.secret_key = 'your-secret-key'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
CREDENTIALS_FILE = 'google-credentials.json'
SHEET_NAME = 'ThongtinthamduTN'
TAB_NAME = 'Trang tính1'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        rsvp_name = request.form.get('rsvp_name')
        rsvp_attend = request.form.get('rsvp_attend')
        rsvp_people = request.form.get('rsvp_people')
        if rsvp_name and rsvp_attend and rsvp_people:
            try:
                creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
                gc = gspread.authorize(creds)
                sh = gc.open(SHEET_NAME)
                worksheet = sh.worksheet(TAB_NAME)
                worksheet.append_row([rsvp_name, rsvp_attend, rsvp_people])
                flash('Thông tin xác nhận đã được lưu thành công!', 'success')
            except Exception as e:
                flash(f'Không thể lưu vào Google Sheets: {str(e)}', 'error')
            return redirect(url_for('home'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)