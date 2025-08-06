from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        sender_name = request.form.get('sender_name')
        recipient_email = request.form.get('recipient_email')
        graduation_date = request.form.get('graduation_date')
        graduation_time = request.form.get('graduation_time')
        location = request.form.get('location')
        message = request.form.get('message')

        try:
            # Tạo nội dung email HTML
            html_content = render_template(
                'email_template.html',
                sender_name=sender_name,
                graduation_date=graduation_date,
                graduation_time=graduation_time,
                location=location,
                message=message
            )

            # Gửi email
            msg = Message(
                'Thư mời dự lễ tốt nghiệp',
                sender=app.config['MAIL_USERNAME'],
                recipients=[recipient_email]
            )
            msg.html = html_content
            mail.send(msg)
            
            flash('Thư mời đã được gửi thành công!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Có lỗi xảy ra: {str(e)}', 'error')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 