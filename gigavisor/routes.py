import os
import secrets
from flask import render_template, url_for, flash, redirect, jsonify, redirect, request, abort
from gigavisor import app, socketio, db, bcrypt
from gigavisor.image import filterIt
from PIL import Image as im
from gigavisor.forms import RegistrationForm, LoginForm
from gigavisor.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send
from datetime import datetime
import glob


#App routes and definitions
@app.route('/')
@app.route("/home")
def home():
    # Get a list of the posts
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route("/about")
def about():
    churro = { "author" : "Isaac Sanchez",
             "date" : "Winter 2020",
             "title" : "About",
             "content" : "This project was developed at Southern Oregon University"
    }
    return render_template('about.html', title='about', churro=churro)
# TODO FIx the paths with absolute paths
def save_picture(postdict):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(postdict['url'])
    print(postdict['url'])
    picture_fn = random_hex + f_ext
    #picture_path = os.path.join(app.root_path, 'static/clips', picture_fn)
    picture_path = "/static/clips/" + picture_fn
    print(picture_path)
    i = im.open("gigavisor/"+postdict['url'][1:])
    x = postdict['x']
    y = postdict['y']
    width = postdict['width']
    height = postdict['height']
    area = (x, y, x + width, y + height)
    trim = i.crop(area)
    if postdict['bw']:
        trim = trim.convert('L')
    trim = filterIt(postdict['filter'], trim)
    trim.save("gigavisor"+picture_path)
    return picture_path, picture_fn

@socketio.on('message')
def handleMessage(clipmsg):
    pic_path, pic_fn = save_picture(clipmsg)
    post = Post(title=pic_fn, content=clipmsg['desc'], author=current_user,
    x = clipmsg['x'], y = clipmsg['y'], width = clipmsg['width'], height = clipmsg['height'],
    original = clipmsg['url'], clip = pic_path)
    db.session.add(post)
    db.session.commit()
    clipmsg['author'] = post.author.username
    clipmsg['date'] = post.date_posted.strftime('%Y-%m-%d')
    clipmsg['clip'] = post.clip
    send(clipmsg, broadcast = True)

# Could be deprecated
@app.route('/clippings')
def clippings():
    posts = Post.query.all()
    return render_template('clippings.html', title='clippings', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
