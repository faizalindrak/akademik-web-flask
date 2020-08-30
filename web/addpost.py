@app.route('/blog/new-post', methods=['POST', 'GET'])
@login_required
def blognewpost():
    form = PostForm()
    date = datetime.datetime.now()
    datefm = date.strftime('%Y-%m-%d')
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Postingan kamu sudah diterbitkan', 'is-success is-light')
        return redirect(url_for('blog'))
    return render_template('blognewpost.html', title='Buat postingan baru', form=form)
