# Flask 1.1.1
# Python 3.7.5

from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from flask_socketio import SocketIO, send
from datetime import datetime
from image import clip

# Create an instance of a Flask app
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# TODO: implement DB
posts = []

#App routes and definitions
@app.route('/')
def home():

    return render_template('index.html', posts=posts)

@app.route("/about")
def about():
    churro = { "author" : "Isaac Sanchez",
             "date" : "Winter 2020",
             "title" : "About",
             "content" : "This project was developed at Southern Oregon University"
    }
    return render_template('about.html', title='about', churro=churro)



@socketio.on('message')
def handleMessage(clipmsg):
    clipmsg['author']="Isaac"
    now = datetime.now()
    clipmsg['date'] = now.strftime("%d/%m/%Y, %H:%M:%S")
    clip(clipmsg)
    posts.append(clipmsg)
    send(clipmsg, broadcast = True)

@app.route('/clippings')
def clippings():

    return render_template('clippings.html', title='clippings', posts=posts)

# Run apps from Python interpreter, in debug mode
if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, host='0.0.0.0', port=5000)


# @app.route('/reqpost', methods=['POST'])
# def processjson():
#     data = request.form.to_dict()
#     data['author']="Isaac"
#     now = datetime.now()
#     data['date'] = now.strftime("%d/%m/%Y, %H:%M:%S")
#     clip(data)
#     print(data)
#     posts.append(data)
#     return jsonify({'result' : 'Success'})
