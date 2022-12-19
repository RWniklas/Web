from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager




app = Flask(__name__)
app.config["SECRET_KEY"]="1234"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"
app.app_context().push()
db = SQLAlchemy(app)
login_manager= LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category="info"


from main import routes