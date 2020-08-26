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
    
makul_dosen = db.Table('makul_dosen',
    db.Column('kode_mk', db.String, db.ForeignKey('makul.kode_mk')),
    db.Column('dosen_id', db.Integer, db.ForeignKey('dosen.dosen_id'))
)
    
class Makul(db.Model):
    kode_mk = db.Column(db.String(20), primary_key=True)
    nama_mk = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    dosen_id = db.relationship('Dosen', secondary=makul_dosen, backref=db.backref('lecture'), lazy='dynamic') #foreign_key
    def __repr__(self):
        return f"Makul('{self.kode_mk}')"
    
class Dosen(db.Model):
    dosen_id = db.Column(db.Integer, primary_key=True)
    nama_dosen = db.Column(db.String(100), nullable=False)
    nidn = db.Column(db.String(20), nullable=True)
    makul_id = db.relationship('Makul', backref=db.backref('lecturer'))
    def __repr__(self):
        return f"Makul('{self.dosen_id}')"
    
"""
class Tugas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul_tugas = db.Column(db.String(200), nullable=False)
    deksripsi = db.Column(db.Text(1000), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False)
    mk_id = db.Column(db.Integer)

class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hari = db.Column(db.DateTime, nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    mk_id = db.Column(db.Integer) #foreign_key
    
class Materi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.String(100))
    counter = db.Column(db.Integer, nullable=False)
    mk_id = db.Column(db.Integer) #foreign key
""" 
    