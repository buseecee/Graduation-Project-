import mysql.connector
from flask import Blueprint, request, redirect, url_for, render_template, session, flash
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def user_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    invalid_email = False
    invalid_password = False
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            if check_password_hash(user[4], password):
                session['user_id'] = user[0]
                return redirect(url_for('views.teacher_login'))
            else:
                invalid_password = True
        else:
            invalid_email = True

        return render_template('login.html', invalid_email=invalid_email, invalid_password=invalid_password)

    return render_template('login.html', invalid_email=invalid_email, invalid_password=invalid_password)


def get_db_connection():
    # MySQL bağlantısı oluşturma
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="classcheck"
    )
    return mydb

def validate_password(password):
    if not (8 <= len(password) <= 16):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    if not re.search(r"[A-Z]", password):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    if not re.search(r"[a-z]", password):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    if not re.search(r"[0-9]", password):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    return None

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        teacher_id=request.form['teacher_id']
        teacher_name = request.form['teacher_name']
        teacher_surname = request.form['teacher_surname']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # Şifre validasyonu
        password_error = validate_password(password)
        if password_error:
            flash(password_error, 'error')
            return redirect(url_for('auth.signup'))

        if password != confirmPassword:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.signup'))

        conn = get_db_connection()
        cursor = conn.cursor()

        # Kullanıcının zaten var olup olmadığını kontrol et
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_teacher = cursor.fetchone()

        if existing_teacher:
            flash('User already exists!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('views.signup'))

        hashed_password = generate_password_hash(password)

        cursor.execute("INSERT INTO users (teacher_id, teacher_name, teacher_surname, email, password) VALUES (%s, %s, %s, %s, %s)", 
                       (teacher_id, teacher_name, teacher_surname, email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('User successfully registered!', 'success')
        return redirect(url_for('views.login'))

    return render_template('signup.html')