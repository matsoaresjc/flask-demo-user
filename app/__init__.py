from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "d*xauhr3_=75%&!(w-$e=_(dr4ldd7p78t4jpxr7n9-#eq*&(t"  # you should make this more random and unique
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:iZ8g9ijCb45Hr7s@localhost/foodiez"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning

UPLOAD_FOLDER = './app/static/uploads'

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # necessary to tell Flask-Login what the default route is for the login page
login_manager.login_message_category = "info"  # customize the flash message category

app.config.from_object(__name__)
from app import views
