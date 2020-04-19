# main.py

#from app import app
#from db_setup import init_db, db_session
from forms import SearchForm, EditForm, LoginForm, PasswordForm
from flask import Flask, flash, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
#from models import Userdata
from tables import Results
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userDataTest.db'
app.secret_key = "password123"

db = SQLAlchemy(app)

engine = create_engine('sqlite:///userDataTest.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    #import models
    Base.metadata.create_all(bind=engine)

class Userdata(db.Model):

    __tablename__ = 'userdata'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the username to satify Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

init_db()
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(Userdata).filter(Userdata.username == user_id).first()
    #return Userdata.get(user_id)

@app.route('/', methods=['GET', 'POST'])
def login():
    
    print(db)
    form = LoginForm()

    if form.validate_on_submit():
        #user = Userdata.query.get(form.username.data)
        user = db_session.query(Userdata).filter(Userdata.username == form.username.data).scalar()
        #password = db_session.query(Userdata).filter(Userdata.password == form.password.data).scalar()
        if user != None:
            #password = db_session.query(Userdata).filter(user.password == form.password.data).scalar()
            #if db_session.query(Userdata).filter(Userdata.password == form.)
            #password = str(user.password)
            #if bcrypt.check_password_hash(password, form.password.data):
            #if password != None:
            if str(user.password) == str(form.password.data):
                user.authenticated = True
                db_session.add(user)
                db_session.commit()
                login_user(user, remember=True)
                flash('Logged in!')
                return redirect('/')
            #pw_hash = bcrypt.generate_password_hash(form.password.data)
            else:
                flash(form.password.data)
                flash(user.password)
                return redirect('/')
        else:
            flash('User not found.')
    """
    if request.method == 'POST':
        return logon(form)
    """
    return render_template('login.html', form=form)
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db_session.add(user)
    db_session.commit()
    logout_user()
    return render_template("logout.html")

@app.route('/search', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        
        if search.data['select'] == 'Username':
            qry = db_session.query(Userdata).filter(
                Userdata.username.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'User_id':
            qry = db_session.query(Userdata).filter(
                Userdata.user_id.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(Userdata)
            results = qry.all()
    else:
        qry = db_session.query(Userdata)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/search')
    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
"""
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():

    form = EditForm(request.form)

    #if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        userdata = Userdata()
        if userdata:
            #if Userdata.query.filter(userdata.username == form.username.data) != None:
            if db_session.query(Userdata).filter(Userdata.username == form.username.data).scalar() != None:
                flash('That username is taken. Please try again.')
                return redirect('/new_user')
            else:
                save_changes(userdata, form, new=True)
                flash('User created successfully!')
                return redirect('/')

    return render_template('new_user.html', form=form)
"""
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():

    form = LoginForm()

    #if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        userdata = Userdata()
        if userdata:
            #if Userdata.query.filter(userdata.username == form.username.data) != None:
            if db_session.query(Userdata).filter(Userdata.username == form.username.data).scalar() != None:
                flash('That username is taken. Please try again.')
                return redirect('/new_user')
            else:
                save_changes(userdata, form, new=True)
                flash('User created successfully!')
                return redirect('/')

    return render_template('new_user.html', form=form)

"""
@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):

    qry = db_session.query(Userdata).filter(
                Userdata.user_id==id)
    userdata = qry.first()

    if userdata:
        form = EditForm(formdata=request.form, obj=userdata)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(userdata, form)
            flash('User updated successfully!')
            return redirect('/')
        return render_template('edit_user.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
"""

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():

    user = current_user
    form = PasswordForm()

    if request.method == 'POST' and form.validate():
        user.password = form.password.data
        db_session.add(user)
        db_session.commit()
        flash('User updated successfully!')
        return redirect('/')

    return render_template('edit_user.html', form=form)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

    qry = db_session.query(Userdata).filter(
        Userdata.user_id==id)
    userdata = qry.first()

    if userdata:
        form = EditForm(formdata=request.form, obj=userdata)
        #if request.method == 'POST' and form.validate():
        if form.validate_on_submit():
            db_session.delete(userdata)
            db_session.commit()

            flash('User deleted successfully!')
            return redirect('/')
        return render_template('delete_user.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)

def save_changes(userdata, form, new=False):

    userdata.username = form.username.data
    userdata.password = form.password.data

    if new:

        db_session.add(userdata)

    db_session.commit()
