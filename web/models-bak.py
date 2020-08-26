from datetime import datetime
from web import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(100), nullable=True, default="lainnya")
    content = db.Column(db.Text(2000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Jadwal(db.Model):
    idMK = db.Column(db.Integer, primary_key=True)
    kodeMK = db.Column(db.String(10), nullable=True)
    mata_Kuliah = db.Column(db.String(50), nullable=True)
    jumlahSKS = db.Column(db.Integer, nullable=True)
    semester = db.Column(db.Integer, nullable=True)
    dosen = db.Column(db.String(50), nullable=True)
    hari = db.Column(db.String(10), nullable=True)
    jam = db.Column(db.String(15), nullable=True)
    kelas = db.Column(db.String(10), nullable=True)
    ruangan = db.Column(db.String(10), nullable=True)
    def __repr__(self):
        return f"Jadwal('{self.kodeMK}', '{self.mata_Kuliah}')"