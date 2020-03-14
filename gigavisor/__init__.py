from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.debug = True
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from gigavisor import routes
