import os
import secrets
import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc, asc    
from web import app, db, bcrypt #web name is optional (folder name)
from web.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, JadwalForm#web is package (a folder with __init__.py)
from web.models import User, Post, Jadwal, Makul, Dosen, Tugas, Materi, makul_dosen, Kelas #web is package (a folder with __init__.py)
from web import login_manager
from functools import wraps
from sqlalchemy import func
from datetime import datetime

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.user_level >= 5:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for('home'))
    return wrap

### HOME PAGE ####

@app.route('/home')
@login_required
def home():
    return render_template('home.html', title="there's no place like home")

@app.route('/')
@login_required
def index():
    return redirect(url_for('home'))

### REGISTER ROUTE ###
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('home2'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Akun {form.username.data} berhasil dibuat!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

### lOGIN ROUTE ###
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('jadwalkuliah_all'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Berhasil Masuk!', 'is-success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('jadwalkuliah_all'))
        else:
            flash('Email atau Kata Sandi salah!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)

@app.route("/metu")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)

def save_picture(form_picture, form_username):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    span = "_"
    x = datetime.datetime.now()
    tanggal = x.strftime("%Y%m%d")
    picture_fn = tanggal+span+form_username + span + random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account-update", methods=['GET', 'POST'])
@login_required
def account_update():
    form = UpdateAccountForm(prevpic=current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, form.username.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Akun anda berhasil diperbarui','is-success is-light')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account-update.html', form=form)

@app.route('/admin/master/dosen')
@admin_required
@login_required
def masterdosen():
    data_dosen = Dosen.query.all()
    return render_template('master-dosen.html', title='Admin - Master Data Dosen', data_dosen=data_dosen)

@app.route('/admin/master/makul')
@login_required
def mastermakul():
    data_mk = Makul.query.order_by(desc(Makul.nama_mk)).all()
    return render_template('master-makul.html', title='Admin - Master Data Mata Kuliah', data_mk=data_mk)

@app.route('/admin/master/user')
@login_required
def masteruser():
    data_user = User.query.all()
    return render_template('master-user.html', title='Admin - Master Data User', data_user=data_user)

@app.route('/jadwalkuliah/')
@login_required
def jadwalkuliah():
    daftarkelas = Kelas.query.filter(Kelas.semester_active==current_user.smstr).all()
    subjects = Makul.query.filter(Makul.semester==current_user.smstr).order_by(asc(Makul.nama_mk)).all()
    jadwal = Jadwal.query.join(Dosen).join(Makul).filter(Makul.semester==current_user.smstr).order_by(asc(Jadwal.hari)).order_by(asc(Makul.nama_mk)).all()
    return render_template('jadwalkuliah.html', title="Jadwal Kuliah", jadwal=jadwal, subjects=subjects, daftarkelas=daftarkelas)

@app.route('/jadwalkuliah/all')
@login_required
def jadwalkuliah_all():
    daftarkelas = Kelas.query.filter(Kelas.semester_active==current_user.smstr).all()
    subjects = Makul.query.filter(Makul.semester==current_user.smstr).order_by(asc(Makul.nama_mk)).all()
    jadwal = Jadwal.query.join(Dosen).join(Makul).filter(Makul.semester==current_user.smstr).order_by(asc(Jadwal.hari)).order_by(asc(Makul.nama_mk)).all()
    return render_template('jadwalkuliah.html', title="Jadwal Kuliah", jadwal=jadwal, subjects=subjects, daftarkelas=daftarkelas)

@app.route('/jadwalkuliah/hari/<int:hari>')
@login_required
def jadwalkuliahhari(hari):
    hari = str(hari)
    daftarkelas = Kelas.query.filter(Kelas.semester_active==current_user.smstr).all()
    subjects = Makul.query.filter(Makul.semester==current_user.smstr).order_by(asc(Makul.nama_mk)).all()
    jadwal = Jadwal.query.join(Dosen).join(Makul).filter(Makul.semester==current_user.smstr).filter(func.strftime('%w',Jadwal.hari)==hari).order_by(asc(Jadwal.hari)).all()
    return render_template('jadwalkuliah.html', title="Jadwal Kuliah", jadwal=jadwal, subjects=subjects, daftarkelas=daftarkelas)

@app.route('/jadwalkuliah/kelas/<kelas>')
@login_required
def jadwalkuliahkelas(kelas):
    kelas = kelas
    daftarkelas = Kelas.query.filter(Kelas.semester_active==current_user.smstr).all()
    subjects = Makul.query.filter(Makul.semester==current_user.smstr).order_by(asc(Makul.nama_mk)).all()
    jadwal = Jadwal.query.join(Dosen).join(Makul).filter(Makul.semester==current_user.smstr).filter(Jadwal.kelas==kelas).order_by(asc(Jadwal.hari)).all()
    return render_template('jadwalkuliah.html', title="Jadwal Kuliah", jadwal=jadwal, subjects=subjects, daftarkelas=daftarkelas)

@app.route('/jadwalkuliah/makul/<mk>')
@login_required
def jadwalkuliahmk(mk):
    mk = mk
    daftarkelas = Kelas.query.filter(Kelas.semester_active==current_user.smstr).all()
    subjects = Makul.query.filter(Makul.semester==current_user.smstr).order_by(asc(Makul.nama_mk)).all()
    jadwal = Jadwal.query.join(Dosen).join(Makul).filter(Makul.semester==current_user.smstr).filter(Makul.kode_mk==mk).order_by(asc(Jadwal.hari)).all()
    return render_template('jadwalkuliah.html', title="Jadwal Kuliah", jadwal=jadwal, subjects=subjects, daftarkelas=daftarkelas)


@app.route('/jadwalkuliah/tambah', methods=['POST','GET'])
@login_required
def jadwalkuliah_tambah():
    form = JadwalForm()
    form.matakuliah.query = Makul.query.filter(Makul.semester==current_user.smstr)
    if form.validate_on_submit():
        hari = form.hari.data+','+form.jam.data
        hari_time = datetime.strptime(hari, '%Y,%m,%d,%H,%M,%S')
        makul = int(form.matakuliah.data[0])
        jadwal = Jadwal(tahun_ajar=form.ta.data, hari=datetime.utcnow(), kelas=form.kelas.data, pertemuan=1, ruang=form.ruang.data, makul_id=form.matakuliah.data, dosen_id=form.dosen.data)
        j1 = Jadwal(tahun_ajar=form.ta.data, hari=hari_time, kelas = "TEST", ruang = form.ruang.data, makul_id =makul, dosen_id = 3)
        db.session.add(j1)
        db.session.commit()
        flash('Jadwal telah ditambahkan', 'is-success is-light')
        return redirect(url_for('jadwalkuliah'))
    return render_template('jadwalkuliah-tambah.html', title="Tambah - Jadwal Kuliah", form=form)


    

@app.route('/tugas')
@login_required
def tugas():
    return render_template('comingsoon.html', title="Daftar Tugas")

@app.route('/darling')
@login_required
def daring():
    return render_template('comingsoon.html', title="Link Daring (Zoom)")

@app.route('/materi')
@login_required
def materi():
    return render_template('comingsoon.html', title="Daftar Materi Kuliah")

@app.route('/blog')
def blog():
    posts = Post.query.order_by(desc(Post.date_posted)).all()
    return render_template('blog.html', title="Blog", posts=posts)

@app.route('/blog/mypost')
@login_required
def mypost():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.date_posted)).all()
    return render_template('blogpostlist.html', title='My Post', posts=posts)

@app.route('/blog/post/<int:post_id>')
def blogdetail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blogdetail.html', title=post.title, post=post)

@app.route('/blog/new-post', methods=['POST', 'GET'])
@login_required
def blognewpost():
    form = PostForm()
    date = datetime.now()
    datefm = date.strftime('%Y-%m-%d')
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Postingan kamu sudah diterbitkan', 'is-success is-light')
        return redirect(url_for('blog'))
    return render_template('blognewpost.html', title='Buat postingan baru', form=form)

@app.route('/blog/<int:post_id>/update', methods=['POST','GET'])
@login_required
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.content = form.content.data
        db.session.commit()
        flash('Postingan kamu telah diperbarui', 'is-success is-light')
        return redirect(url_for('mypost', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.content.data = post.content
    return render_template('blognewpost.html', title='Update Post', form=form)

@app.route('/blog/<int:post_id>/delete')
@login_required
def deletepost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Postingan kamu telah dihapus', 'is-danger is-light')
    return redirect(url_for('mypost'))

@app.route('/modal')
def modal():
    return render_template('modal.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Anda harus login terlebih dahulu', 'danger is-light')
    return redirect('/login')

