import mysql.connector
from flask import Blueprint, request, redirect, url_for, render_template, session, flash
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def get_db_connection():
    # MySQL bağlantısı oluşturma
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="classcheck"
    )
    return mydb

def fetch_teachers():
    # Veritabanı bağlantısını kur
    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL sorgusunu çalıştır ve veriyi çek
    cursor.execute("SELECT teacherid, teachername, teacheremail FROM teachers")
    rows = cursor.fetchall()

    # Bağlantıyı kapat
    connection.close()

    return rows

@auth.route('/login', methods=['POST'])
def login():
    invalid_email = False
    invalid_password = False
    email = request.form['teacheremail']
    password = request.form['teacherpassword']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE teacheremail=%s AND teacherpassword=%s", (email, password))
    teacher = cursor.fetchone()

    if teacher:
        # Giriş başarılıysa ana sayfaya yönlendir
        return redirect(url_for('views.teacher_login'))
    else:
        # Giriş başarısızsa hata mesajıyla birlikte login sayfasına yönlendir
        return render_template('login.html', invalid_login=True, invalid_email=True, invalid_password=True)

@auth.route('/show_teachers')
def show_teachers():
    teachers = fetch_teachers()
    return render_template('teachers.html', teachers=teachers)
    
