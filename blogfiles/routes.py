from blogfiles import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from blogfiles.forms import RegistrationForm, LoginForm, AccountForm, PostForm, LearnForm
from blogfiles.models import User, Post, Learn
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import os
from PIL import Image

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    posts.reverse()
    learns = Learn.query.all()
    return render_template('home.html', posts=posts, learns=learns, title='Hír', todo_title="Teendők:")


def save_image(image_form):
    f_fn = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_form.filename)
    image_fn = f_fn + f_ext
    image_path = os.path.join(app.root_path, 'static/profil_pics/', image_fn)
    i = Image.open(image_form)
    i_size = (96, 96)
    i.thumbnail(i_size)
    i.save(image_path)

    return image_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.default_image.data:
            img_fn = 'default.png'
            current_user.image = img_fn
        else:
            if form.image.data != None:
                img_fn = save_image(form.image.data)
                current_user.image = img_fn
            else:
                img_fn = current_user.image
        db.session.commit()
        flash('Fiókod frissítve', 'success')
        return redirect(url_for('account'))

    return render_template('account.html', form=form, title='Account')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        reg_user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(reg_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('registration.html', form=form, title='Regisztráció')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            flash('Rossz felhasználónév vagy jelszó', 'danger')

    return render_template('login.html', form=form, title='Bejelentkezés')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    logout_user()
    return redirect(url_for('login'))


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get(int(post_id))

    return render_template('post.html', post_id=post.id, post=post, title='Post')

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        create_post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        
        db.session.add(create_post)
        db.session.commit()
        
        return redirect(url_for('home'))
        
    return render_template('create_post.html', form=form, title='Új post', post=False)

@app.route('/update_post/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    form = PostForm()
    post = Post.query.get(int(post_id))
    posts = list(Post.query.all())
    
    if current_user.username == post.author.username or current_user.rank == 9:
        
        if request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content

        if form.validate_on_submit():                
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            

            return redirect(url_for('home'))
            
        return render_template('create_post.html', post_id=post.id, post=post, form=form, title='Post szerkesztése')
    
    else:
        return redirect(url_for('home'))

@app.route('/delete_post/<post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get(int(post_id))
    if current_user.username == post.author.username or current_user.rank == 9:
        db.session.delete(post)
        db.session.commit()
        print(Post.query.all())
        
        return redirect(url_for('home'))
    
    else:
        return redirect(url_for('home'))
    
@app.route('/edit_learn', methods=['GET', 'POST'])
def edit_learn():
    if current_user.rank == 9:
        learns = Learn.query.all()
        form = LearnForm()

        if form.validate_on_submit():
            new_learn = Learn(desc=form.desc.data)
            db.session.add(new_learn)
            db.session.commit()
            
            return redirect(url_for('edit_learn'))
        
        return render_template('learn.html', learns=learns, form=form, title="Teendők:")
    
    else:
        return redirect(url_for('home'))
    
    


@app.route('/delete_learn/<learn_id>', methods=['GET', 'POST'])
def delete_learn(learn_id):
    if current_user.rank == 9:
        learn = Learn.query.get(int(learn_id))  
        db.session.delete(learn)  
        db.session.commit()
    else:
        return redirect(update_post('home'))
    
    return redirect(url_for('edit_learn'))
    
    