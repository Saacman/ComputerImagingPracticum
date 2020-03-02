from flask import render_template, url_for, flash, redirect, jsonify
from gigavisor import app, socketio
from gigavisor.image import clip
from flask_socketio import send
from datetime import datetime
import glob


# TODO: implement DB, post imag, etc
posts = []

#App routes and definitions
@app.route('/')
def home():
    #gall = glob.glob("static/images/*.jpg")
    #print(gall)
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
    # Add to DB ???
    posts.append(clipmsg)
    send(clipmsg, broadcast = True)


@app.route('/clippings')
def clippings():
    return render_template('clippings.html', title='clippings', posts=posts)



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
