import mysql.connector
from flask import Blueprint, request, redirect, url_for, render_template,jsonify, session, flash
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)
# Orijinal şifreyi hashleme
hashed_password = generate_password_hash("00Be1414.")

# Veritabanına eklerken bu hashed_password'ü kullanmalısınız.
print(hashed_password)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  # MySQL sunucunuzun adresi
        user='buse',  # MySQL kullanıcı adı
        password='123456.',  # MySQL şifresi
        database='classcheck' # Kullanmak istediğiniz veritabanı
    )
    return conn

def user_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    invalid_email = False
    invalid_password = False
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE email=%s", (email,))
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

    return render_template('login.html', invalid_email=True, invalid_password=True)

@auth.route('/logout')
def logout():
    # Kullanıcı oturumunu sonlandır
    session.pop('user_id', None)
    session.pop('user_email', None)
    return redirect(url_for('views.login'))
    
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        teacher_id=request.form['teacher_id']
        teacher_name = request.form['teacher_name']
        teacher_surname = request.form['teacher_surname']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirm_password']

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
        cursor.execute("SELECT * FROM teachers WHERE email=%s", (email,))
        existing_teacher = cursor.fetchone()

        if existing_teacher:
            flash('User already exists!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('views.signup'))

        hashed_password = generate_password_hash(password)

        cursor.execute("INSERT INTO teachers (teacher_id, teacher_name, teacher_surname, email, password) VALUES (%s, %s, %s, %s, %s)", 
                       (teacher_id, teacher_name, teacher_surname, email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('User successfully registered!', 'success')
        return redirect(url_for('views.login'))

    return render_template('signup.html')

       
        
        

@auth.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        course_day = request.form['course_day']
        lesson_start_time= request.form['lesson_start_time']
        lesson_end_time= request.form['lesson_end_time']
        class_name = request.form['class_name']
        
        # Boş alan kontrolü
        if not course_id or not course_name or not course_day or not lesson_start_time or not lesson_end_time or not class_name:
            return jsonify({'success': False, 'message': 'All fields are required!'})
        
        # Veritabanına ekleme
        conn = get_db_connection()
        cursor = conn.cursor()

        # Kursun zaten var olup olmadığını kontrol et
        cursor.execute("SELECT * FROM courses WHERE course_id=%s", (course_id,))
        existing_course = cursor.fetchone()
        
        if existing_course:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Course already exists!'})
    
        cursor.execute("INSERT INTO courses (course_id, course_name, course_day, lesson_start_time, lesson_end_time, class_name) VALUES (%s, %s, %s, %s, %s, %s)", (course_id, course_name, course_day, lesson_start_time, lesson_end_time, class_name))
        conn.commit()
        cursor.close()
        conn.close()
    
    return jsonify({'success': True, 'message': 'Course successfully added!'})

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


@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        # Kullanıcının oturum bilgilerini al
        user_id = session.get('user_id')
        
        if not user_id:
            return redirect(url_for('auth.login'))

        # Veritabanından mevcut şifreyi kontrol et
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM teachers WHERE id=%s", (user_id,))
        teacher = cursor.fetchone()
        
        # Mevcut şifreyi kontrol et
        if not teacher or not check_password_hash(teacher['password'], current_password):
            conn.close()
            error = "Current password is incorrect."
            return render_template('change_password.html', error=error)
        
        # Yeni şifreyi hashle ve güncelle
        hashed_new_password = generate_password_hash(new_password)
        cursor.execute("UPDATE teachers SET password=%s WHERE id=%s", (hashed_new_password, user_id))
        conn.commit()
        conn.close()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('auth.change_password'))
    
    return render_template('change_password.html')

