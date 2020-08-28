from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, TextAreaField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from web.models import User #web is package name (a folder with __init__.py)


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

class TambahJadwal(FlaskForm):
    kodeMK = StringField('Kode Mata Kuliah', validators=[DataRequired()])
    mataKuliah = StringField('Mata Kuliah', validators=[DataRequired()])
    jumlahSKS = SelectField('Jumlah SKS', choices=[(2,2),(3,3),(4,4),(5,5),(6,6)])
    semester = SelectField('Semester', choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)], validators=[DataRequired()])
    dosen = StringField('Nama Dosen', validators=[DataRequired()])
    hari = SelectField('Hari', choices=[('Senin','Senin'),('Selasa','Selasa'),('Rabu','Rabu'),('Kamis','Kamis'),('Jumat','Jumat '),('Sabtu','Sabtu')], validators=[DataRequired()])
    jam = SelectField('Waktu', choices=[('08.00 - 10.00','08.00 - 10.00'), ('10.00 - 12.00', '10.00 - 12.00'), ('12.00 - 14.00', '12.00 - 14.00'),('16.00 - 18.00', '16.00 - 18.00'), ('18.00 - 20.00', '18.00 - 20.00'), ('20.00 - 22.00', '20.00 - 22.00')], validators=[DataRequired()])
    kelas = StringField('Kelas', validators=[DataRequired()])
    ruangan = StringField('Ruangan', validators=[DataRequired()])
    submit = SubmitField('Tambahkan')   