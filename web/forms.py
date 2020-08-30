from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, TextAreaField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from web import app, db
from web.models import User, Kelas, Makul, Dosen  #web is package name (a folder with __init__.py)
from sqlalchemy import desc, asc   

class RegistrationForm(FlaskForm):
    username = StringField('Nama Pengguna', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Kata Sandi', validators=[DataRequired()])
    confirm_password = PasswordField('Konfirmasi Kata Sandi', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Daftar Sekarang!')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nama pengguna sudah dipakai')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email sudah pernah dipakai')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Kata Sandi', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log Masuk')

class UpdateAccountForm(FlaskForm):
    username = StringField('Nama Pengguna', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Upload Foto Profile Baru', validators=[FileAllowed(['jpg', 'png'])])
    prevpic = HiddenField()
    submit = SubmitField('Simpan perubahan')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Nama pengguna sudah dipakai')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email sudah pernah dipakai')

class PostForm(FlaskForm):
    title = StringField('Judul Postingan', validators=[DataRequired()])
    category = SelectField('Kategori',default='lainnya', choices=[('Pengumuman', 'Pengumuman'),('Pengetahuan', 'Pengetahuan'), ('Pengetahuan', 'Ekstra'),('Lainnya','Lainnya')])
    content = TextAreaField('Konten', validators=[DataRequired()])
    submit = SubmitField('Posting')

class UpdatePostForm(FlaskForm):
    title = StringField('Judul Postingan', validators=[DataRequired()])
    content = TextAreaField('Konten', validators=[DataRequired()])
    submit = SubmitField('Posting')

def makul_query():
    return Makul.query

class JadwalForm(FlaskForm):
    ta = StringField('Tahun Ajar', validators=[DataRequired()])
    hari = SelectField('Hari', choices=[('2020,8,24', 'Senin'),('2020,8,25','Selasa'),('2020,8,26', 'Rabu'),('2020,8,27','Kamis'),('2020,8,28','Jumat'),('2020,8,29','Sabtu')])
    jam = SelectField('Jam', choices=[('8,00,00','08:00'),('10,00,00','10:00'),('12,00,00','12:00'),('14,00,00','14:00'),('16,00,00','16:00'),('18,00,00','18:00'),('20,00,00','20:00')])
    kelas = QuerySelectField(label="Kelas", validators=[DataRequired()], query_factory=lambda: db.session.query(Kelas).filter(Kelas.semester_active==current_user.smstr), get_pk=lambda nama_kelas:nama_kelas, get_label=lambda nama_kelas:nama_kelas, allow_blank=True)
    ruang = StringField('Ruang', validators=[DataRequired()])
    matakuliah = QuerySelectField(label="Mata Kuliah", query_factory=makul_query, get_label='nama_mk', allow_blank=True)
    dosen = QuerySelectField(label="Dosen Pengampu", validators=[DataRequired()], query_factory=lambda: db.session.query(Dosen).order_by(asc(Dosen.nama_dosen)), get_pk=lambda dosen_id:dosen_id, get_label='nama_dosen')
    submit = SubmitField('Tambah Jadwal')
