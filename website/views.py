from flask import Blueprint,render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('base.html')

@views.route('/authorized_login')
def authorized_login():
    return render_template('authorized_login.html')

@views.route('/teacher_login')
def teacher_login():
    return render_template('teacher_login.html')

# Diğer görünüm fonksiyonları buraya eklenebilir