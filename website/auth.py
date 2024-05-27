import sqlite3
from flask import Blueprint, request
import os

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return '<p>Login Page</p>'

def get_db_connection():
    conn = sqlite3.connect('C:/Users/Buse Ece/Desktop/sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn

@auth.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']
    confirm_password=request.form['confirm_password']

    conn = get_db_connection()
    
      # SELECT sorgusu için yeni bir cursor oluşturuyoruz
    select_cursor = conn.cursor()
    select_cursor.execute("SELECT * FROM teacher WHERE NAME=?", (name,))

    # SELECT sorgusu sonucunu alıyoruz
    existing_record = select_cursor.fetchone()
 # Eğer kayıt varsa hata ver ve işlemi sonlandır
    if existing_record:
        select_cursor.close()
        conn.close()
        return 'User already exists!'
    
    # SELECT sorgusu için kullandığımız cursor'ı kapatıyoruz
    select_cursor.close()
    
    # INSERT işlemi için yeni bir cursor oluşturuyoruz
    insert_cursor = conn.cursor()
    
    # INSERT sorgusunu çalıştırıyoruz
    insert_cursor.execute("INSERT INTO teacher (name, surname, email, password, confirm_password) VALUES (?, ?, ?, ?, ?)", (name, surname, email, password, confirm_password))
    
    # İşlemi tamamla ve bağlantıyı kapat
    conn.commit()
    conn.close()
    
    return 'Sign up successful!'
