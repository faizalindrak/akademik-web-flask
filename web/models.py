from datetime import datetime
from web import db, login_manager
from flask_login import UserMixin
import locale 
locale.setlocale(locale.LC_ALL, 'id_ID')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    user_level = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=False)
    angkatan = db.Column(db.String(4))
    kurikulum = db.Column(db.String(10))
    posts = db.relationship('Post', backref='author', lazy=True)
    profiles = db.relationship('Profile', backref='user', lazy=True, uselist=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Profile(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nama_depan = db.Column(db.String(20))
    nama_belakang = db.Column(db.String(20))
    tempat_lahir = db.Column(db.String(50))
    tanggal_lahir = db.Column(db.DateTime)
    nim = db.Column(db.String(20))
    no_anggota = db.Column(db.String(20))
    kelas = db.Column(db.String(5))
    jenis_kelamin = db.Column(db.String(20))
    agama = db.Column(db.String(20))
    no_hp = db.Column(db.String(20))
    alamat = db.Column(db.String(200))
    def __repr__(self):
        return f"User('{self.profile_id}', '{self.nama_depan}', '{self.kelas}')"
    def get_ulevel(self):
        return self.ulevel
    
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
    db.Column('kode_mk', db.String(20),db.ForeignKey('makul.makul_id'), primary_key=True),
    db.Column('dosen_id', db.Integer, db.ForeignKey('dosen.dosen_id'), primary_key=True))
    
class Makul(db.Model):
    makul_id = db.Column(db.Integer, primary_key=True)
    kode_mk = db.Column(db.String(20))
    kurikulum = db.Column(db.String(5))
    nama_mk = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    jenis_mk = db.Column(db.String(5))
    jadwal_makul = db.relationship('Jadwal', backref='subject', lazy=True)
    tugas_makul = db.relationship('Tugas', backref='task', lazy=True)
    materi_makul = db.relationship('Materi', backref='docs', lazy=True)
    def __repr__(self):
        return f"Makul('{self.kode_mk}', '{self.nama_mk}')"
    
class Dosen(db.Model):
    dosen_id = db.Column(db.Integer, primary_key=True)
    nama_dosen = db.Column(db.String(100), nullable=False)
    nidn = db.Column(db.String(20), nullable=True)
    jadwal_dosen = db.relationship('Jadwal', backref='lecturer', lazy=True)
    tugas_dosen = db.relationship('Tugas', backref='penugas', lazy=True)
    materi_dosen = db.relationship('Materi', backref='pemateri', lazy=True)
    subjects = db.relationship('Makul', secondary=makul_dosen, backref=db.backref('lecturers'))
    def __repr__(self):
        return f"Dosen('{self.dosen_id}', '{self.nama_dosen}'')"
    
class Jadwal(db.Model):
    jadwal_id = db.Column(db.Integer, primary_key=True)
    hari = db.Column(db.DateTime, nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    ruang = db.Column(db.String(10), nullable=False)
    pertemuan = db.Column(db.Integer)
    makul_id = db.Column(db.String(20), db.ForeignKey('makul.kode_mk'))
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.dosen_id'))
    def __repr__(self):
        return f"Jadwal('{self.jadwal_id}')"
    

class Tugas(db.Model):
    tugas_id = db.Column(db.Integer, primary_key=True)
    judul_tugas = db.Column(db.String(200), nullable=False)
    deksripsi = db.Column(db.Text(1000), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False)
    makul_id = db.Column(db.String(20), db.ForeignKey('makul.kode_mk'))
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.dosen_id'))
    def __repr__(self):
        return f"Tugas('{self.tugas_id}')"
    
class Materi(db.Model):
    materi_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    remarks = db.Column(db.String(100))
    counter = db.Column(db.Integer)
    makul_id = db.Column(db.String(20), db.ForeignKey('makul.kode_mk'))
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.dosen_id'))
    def __repr__(self):
        return f"Materi('{self.materi_id}')"

    