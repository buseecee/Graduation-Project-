from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return '<p>Login Page</p>'

@auth.route('/register')
def register():
    return 'Register Page'



# Diğer kimlik doğrulama işlevleri buraya eklenebilir

