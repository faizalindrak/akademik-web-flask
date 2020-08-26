from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ee54d50dce6cfc33d73996045cf23ccc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
from models import User,Post


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Akun {form.username.data} berhasil dibuat!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@localhost.loc' and form.password.data == 'password':
            flash('Berhasil masuk', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email atau Kata Sandi salah!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)

@app.route('/home2', methods=['GET', 'POST'])
def home2():
    return render_template('index2.html', title='after login')


if __name__ == "__main__":
    app.run(debug=True)