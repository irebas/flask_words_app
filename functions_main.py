from models import *
from vars_libs import *


@app.route('/index.html', methods=['GET'])
@app.route('/')
def index():
    """
    :return: if user is logged returns index, otherwise login
    :rtype: page
    """
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/login.html', methods=["POST", "GET"])
def login():
    """
    :return: Clears session. If user exists in DB and provided username and password are correct redirects to index
    and sets session['username'] to username, otherwise redirect to login page.
    """
    session.clear()
    if request.method == 'POST':
        if request.form.get('login'):
            username = request.form['username']
            password = request.form['password']
            user_db = Users.query.filter(Users.username == username).first()
            if not user_db:
                flash('Wrong username')
                return render_template('login.html')
            else:
                if user_db.password == password:
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    flash('Wrong password')
                    return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/sign_up.html', methods=["POST", "GET"])
def sign_up():
    """
    :return: if username or email doesn't exist in DB, creates new user and redirects to index.
    Sets session['username'] to created user.
    """
    if request.method == 'POST':
        if request.form.get('signup'):
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            user_db = Users.query.filter(Users.username == username).first()
            email_db = Users.query.filter(Users.email == email).first()
            if (not user_db) and (not email_db):
                user = Users(username, password, email, 'user')
                db.session.add(user)
                db.session.commit()
                flash('User created')
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('User already exists!')
                return render_template('sign_up.html')
    else:
        return render_template('sign_up.html')


@app.route('/view_users.html', methods=['POST', 'GET'])
def view_users():
    """
    :return: table with users.
    """
    user_type = Users.query.filter(Users.username == session['username']).first().user_type
    if user_type == 'admin':
        users = Users.query.order_by(Users.username.asc()).all()
        return render_template('/view_users.html', users=users)
    else:
        flash('Access denied')
        return render_template('/view_users.html')
