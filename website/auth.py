import mysql.connector
from flask import Blueprint, request, redirect, url_for, render_template, session, flash
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  # MySQL sunucunuzun adresi
        user='buse',  # MySQL kullanıcı adı
        password='123456.',  # MySQL şifresi
        database='classcheck'  # Kullanmak istediğiniz veritabanı
    )
    return conn


@auth.route('/login', methods=['POST'])
def login():
    invalid_email = False
    invalid_password = False
    email = request.form['email']
    password = request.form['password']
    
    # Veritabanından e-posta ve şifre kontrolü
    conn=get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE email=%s AND password=%s", (email, password))
    teacher = cursor.fetchone()

    if teacher:
        # Giriş başarılıysa ana sayfaya yönlendir
        return redirect(url_for('views.teacher_login'))
    else:
        # Giriş başarısızsa hata mesajıyla birlikte login sayfasına yönlendir
        return render_template('login.html', invalid_login=True, invalid_email=True, invalid_password=True)

    """ @auth.route('/teacher_login')
def get_students_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, surname FROM students_info")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('teacher_login.html', students=students) """

    """ @auth.route('/login', methods=['GET', 'POST'])
def login():
    invalid_email = False
    invalid_password = False
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE email=?", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('login.html') """
    """ if user:
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                return redirect(url_for('views.teacher_login'))
            else:
                invalid_password = True
        else:
            invalid_email = True """

    """ return render_template('login.html', invalid_email=invalid_email, invalid_password=invalid_password)

    return render_template('login.html', invalid_email=invalid_email, invalid_password=invalid_password) """

    """ def validate_password(password):
    if not (8 <= len(password) <= 16):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    if not re.search(r"[A-Z]", password):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    if not re.search(r"[a-z]", password):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    if not re.search(r"[0-9]", password):
        return "Your password must be 8-16 characters, include at least one lowercase letter, one uppercase letter, and a number."
    return None """

    """ @auth.route('/signup', methods=['GET', 'POST'])
    def signup():
    if request.method == 'POST':
        # POST isteği ile gelen verileri işleme kodları
        pass
    else:
        # GET isteği ile signup sayfasını render etme kodları
        return render_template('signup.html')
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']

    # Şifre validasyonu
    if not email.endswith('@aydin.edu.tr'):
        flash('Invalid email domain. Only @aydin.edu.tr emails are allowed.')
        return redirect(url_for('auth.signup_page'))

    password_error = validate_password(password)
    if password_error:
        flash(password_error)
        return redirect(url_for('auth.signup_page'))
    
    if password != confirmPassword:
        flash('Passwords do not match.')
        return redirect(url_for('auth.signup_page'))

    conn = get_db_connection()
    try:
        # Kullanıcı var mı kontrol et
        select_cursor = conn.cursor()
        select_cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_record = select_cursor.fetchone()
        select_cursor.close()

        if existing_record:
            return 'User already exists!'
        
        # Yeni kullanıcı ekle
        insert_cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        insert_cursor.execute(
            "INSERT INTO users (name, surname, email, password) VALUES (%s, %s, %s, %s)",
            (name, surname, email, hashed_password)
        )
        conn.commit()
        insert_cursor.close()
        
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        conn.close() """

    """     # INSERT işlemi için yeni bir cursor oluşturuyoruz
    insert_cursor = conn.cursor()
    
    # INSERT sorgusunu çalıştırıyoruz
    insert_cursor.execute("INSERT INTO teacher (name, surname, email, password, confirmPassword) VALUES (%s, %s, %s, %s, %s)", (name, surname, email, password, confirmPassword))
    
    # İşlemi tamamla ve bağlantıyı kapat
    conn.commit()
    conn.close()
    
    return 'Sign up successful!' """


