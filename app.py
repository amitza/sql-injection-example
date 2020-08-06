import flask
from flask.helpers import flash, url_for
from flask.wrappers import Response
from flask_login.utils import current_user, login_required
from LoginForm import LoginForm
import os
import mysql.connector
from flask import render_template, redirect, request
import flask_login
from user import User

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

connection = mysql.connector.connect(
    user='root', password='admin', database='bank')


@login_manager.user_loader
def user_loader(user_id):
    """Check if user is logged-in upon page load."""
    print('check if user logged in')
    if user_id is not None:
        return get_user_by_id(user_id)
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if flask.request.method == 'POST':
        with connection.cursor(buffered=True) as cursor:
            try:
                results = cursor.execute("SELECT * FROM account WHERE email='%s'" %
                                     flask.request.values['email'], multi=True)
                response = []
                for cur in results:
                    if cur.with_rows:
                        response.append(str(cur.fetchall()))

                return Response(status=200, response=response)  
            except Exception as e:
                return Response(status=500, response=e.msg)

    if flask.request.method == 'GET':
        return render_template(
            'login.jinja2',
            form=form,
            title='Log in.',
            template='login-page',
            body="Log in with your User account.")

    # if form.validate_on_submit():
    #     user = get_user_by_email(email=form.email.data)
    #     if user and user.password == form.password.data:
    #         flask_login.login_user(user)
    #         return flask.redirect('/search')
    #     flash('Invalid username/password combination')
    #     return redirect('/login')


@ app.route('/search')
@ flask_login.login_required
def protected():
    print('Logged in as: ' + flask_login.current_user.id)
    username = request.args.get('username')
    return render_template(
        'dashboard.jinja2',
        title='Flask-Login Tutorial.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!")


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@ login_manager.unauthorized_handler
def unauthorized_handler():
    flash('You must be logged in to view that page.')
    return 'Unauthorized'


def get_user_by_id(user_id: str):
    with connection.cursor(buffered=True) as cursor:
        iterator = cursor.execute("SELECT * FROM account WHERE userid='%s'" %
                                  user_id, multi=True)

        for res in iterator:
            row = res.fetchone()
            return User(
                name=row[0],
                id=row[1],
                password=row[2],
                balance=row[3],
                email=row[4],
                contactno=row[5])


def get_user_by_email(email: str):
    with connection.cursor(buffered=True) as cursor:
        iterator = cursor.execute("SELECT * FROM account WHERE email='%s'" %
                                  email, multi=True)

        for res in iterator:
            row = res.fetchone()
            if row is None:
                return None
            return User(
                name=row[0],
                id=row[1],
                password=row[2],
                balance=row[3],
                email=row[4],
                contactno=row[5])
