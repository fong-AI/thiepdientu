import gspread
from google.oauth2.service_account import Credentials

# Định nghĩa scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Đường dẫn đến file thông tin xác thực
CREDENTIALS_FILE = 'google-credentials.json'
SHEET_NAME = 'ThongtinthamduTN'
TAB_NAME = 'Trang tính1'

try:
    # Xác thực bằng tài khoản dịch vụ
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)

    # Mở Google Sheet
    sh = gc.open(SHEET_NAME)
    worksheet = sh.worksheet(TAB_NAME)

    # Thêm một dòng thử nghiệm
    worksheet.append_row(['Test', 'Test', 'Test'])
    print('Ghi thành công!')

except gspread.exceptions.APIError as e:
    print(f"Lỗi API: {e}")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")