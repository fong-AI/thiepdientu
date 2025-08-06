from flask import Flask, render_template, request, flash, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SHEET_NAME = 'ThongtinthamduTN'
TAB_NAME = 'Trang tính1'

def get_credentials():
    try:
        # Lấy JSON từ biến môi trường và parse trực tiếp
        credentials_json = os.environ.get('GOOGLE_CREDENTIALS')
        if not credentials_json:
            raise ValueError("Biến môi trường GOOGLE_CREDENTIALS không được thiết lập")
        credentials_dict = json.loads(credentials_json)
        return Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
    except Exception as e:
        raise Exception(f"Lỗi khi lấy credentials: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        rsvp_name = request.form.get('rsvp_name')
        rsvp_attend = request.form.get('rsvp_attend')
        rsvp_people = request.form.get('rsvp_people')
        if rsvp_name and rsvp_attend and rsvp_people:
            try:
                creds = get_credentials()
                gc = gspread.authorize(creds)
                sh = gc.open(SHEET_NAME)
                worksheet = sh.worksheet(TAB_NAME)
                worksheet.append_row([rsvp_name, rsvp_attend, rsvp_people])
                flash('Thông tin xác nhận đã được lưu thành công!', 'success')
            except Exception as e:
                print(f"Lỗi khi lưu vào Google Sheets: {str(e)}")  # In lỗi để debug
                flash(f'Không thể lưu vào Google Sheets: {str(e)}', 'error')
            return redirect(url_for('home'))
        else:
            flash('Vui lòng điền đầy đủ thông tin', 'error')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
