from flask import Flask, request, render_template, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# SQLAlchemy database setup
engine = create_engine('sqlite:///../translations.db')  # Replace with your database URI
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/')
def home():
    if 'username' in session:
        return f'Logged in as {session["username"]}. <a href="/logout">Logout</a>'
    return 'You are not logged in. <a href="/login">Login</a> or <a href="/register">Register</a>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        session = Session()
        user = User(username=username, email=email, password=hashed_password.decode('utf-8'))
        session.add(user)
        session.commit()
        session.close()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the entered password and compare it to the stored hash
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['username'] = username
            session_.close()
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your username and password.')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
