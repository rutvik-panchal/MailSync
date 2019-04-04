from flask import render_template,redirect,url_for,flash,request,session
from myproject import db,app
from myproject.models import users
from myproject.forms import loginForm,RegistrationForm,sendMailForm
from flask_login import login_user,login_required,logout_user,LoginManager
from myproject.methods import sendMail,getMail,checkAuth,getSent,getTrash,toMarkup
from flask import Markup
from werkzeug import secure_filename
import os

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome',methods=['GET', 'POST'])
@login_required
def welcome_user():
    username = session['username']
    password = session['password']
    form = sendMailForm()

    if form.validate_on_submit():
        f = form.att.data
        f.save(f.filename)
        sendMail(username,password,form.to.data,form.subject.data,form.body.data,form.att.data.filename)
        form.to.data=''
        form.subject.data=''
        form.body.data=''
        os.remove(form.att.data.filename)
    data = getMail(username,password)
    title = "inbox"

    #bodyCheck = toMarkup(data[1])

    return render_template('userpage.html',form=form,sender=data[0],body=data[1],title = title)

@app.route('/sent',methods=['GET', 'POST'])
@login_required
def showsent():
    username = session['username']
    password = session['password']
    form = sendMailForm()
    data = getSent(username,password)
    if form.validate_on_submit():
        sendMail(username,password,form.to.data,form.subject.data,form.body.data)
        form.to.data=''
        form.subject.data=''
        form.body.data=''
    title = "sent"

    return render_template('userpage.html',form=form,sender=data[0],body=data[1],title = title,len = 2)

@app.route('/trash',methods=['GET', 'POST'])
@login_required
def showtrash():
    username = session['username']
    password = session['password']
    form = sendMailForm()
    data = getTrash(username,password)
    if form.validate_on_submit():
        sendMail(username,password,form.to.data,form.subject.data,form.body.data)
        form.to.data=''
        form.subject.data=''
        form.body.data=''
    title = "trash"

    return render_template('userpage.html',form=form,sender=data[0],body=data[1],title = title)

@app.route('/logout')
@login_required
def logout():
    session.pop('password', None)
    session.pop('username', None)
    logout_user()
    flash("you are logged out")

    return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
    form = loginForm()
    if form.validate_on_submit:
        user = users.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data) :
            session['username'] = form.email.data
            session['password'] = form.password.data
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
            return redirect(url_for('welcome_user'))

    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    validation = 0
    if form.validate_on_submit():
        if(checkAuth(form.email.data,form.password.data)==1):
            user = users(name=form.name.data,
                     email=form.email.data,
                     password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash("Thanks for registation!")
            return redirect(url_for('login'))
        else:
            validation = 1

    return render_template('register.html',form=form,validation = validation)


if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0')
