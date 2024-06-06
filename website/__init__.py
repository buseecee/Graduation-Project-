from flask import Flask, render_template
from .auth import auth
from .views import views

def create_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    # Blueprint importu
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

   # @app.route('/')
   # def authorized_login():
       # return render_template('authorized_login.html') 

    return app
