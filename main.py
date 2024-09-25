from __future__ import annotations
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship
from sqlalchemy import Integer, String, ForeignKey
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from webform import ListForm, Login, Registration
from data import Data
from flask_login import LoginManager, UserMixin, login_required, current_user, logout_user, login_user
import os
from typing import List

# instances

app = Flask(__name__)
app.secret_key = os.environ.get('secret_key')

bootstrap = Bootstrap5(app)
data = Data()
login_manager = LoginManager()

# configure login_manager  for login
login_manager.init_app(app)


# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


#
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# initialize the app with the extension
db.init_app(app)


# Model Table
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[int] = mapped_column(Integer(), nullable=False)
    # This will act like a List of Task objects attached to each User.
    # The "user" refers to the author property in the TaskSchedule class.
    task_schedule: Mapped[List['TaskSchedule']] = Relationship(back_populates='user')


class TaskSchedule(db.Model):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    task_date: Mapped[str] = mapped_column(String(20), nullable=False)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    # Create reference to the User object. The "task_schedule" refers to the task_schedule property in the User class.
    user: Mapped['User'] = Relationship(back_populates='task_schedule')


# create table
with app.app_context():
    db.create_all()


@app.route('/schedule', methods=['GET', 'POST'])
def schedule_task():
    # form obj

    form = ListForm()

    # validated user inputs on submit

    if form.validate_on_submit():
        # add task
        task = data.add_task(task_name=form.task.data, task_date=form.time.data)

        return redirect(url_for('schedule_task'))

    year = datetime.now().year
    return render_template('schedule.html', form=form, year=year, tasklist=data.task_list)


@app.route('/')
def home():
    return render_template('index.html', )


@app.route('/delete/', methods=['GET', 'POST'])
def delete_task():
    task_id = int(request.args.get('id'))
    print(task_id)

    data.remove_task(task_id)
    return redirect(url_for('schedule_task'))


@app.route('/login', methods=['GET', 'POST'])
def signin():
    form = Login()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.username == form.username.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('signin'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('signin'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template('signin.html', form=form, game=True)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        # Hashing and salting the password entered by the user
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        # Storing the hashed password in our database
        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password=hash_and_salted_password,
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('schedule_task'))

    return render_template("signup.html", form=form, game=True)


if __name__ == '__main__':
    app.run(debug=True)
