from flask import redirect, url_for, render_template, flash, request
from main.models import User, Post, Comment,Like
from main import app, db
from PIL import Image
from main.form import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SearchForm 
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
bcrypt = Bcrypt(app)

app.jinja_env.globals.update(clever_function=SearchForm)

def search():

    if request.method=="POST":
        print("test1")
      
    
        search= request.form["search"]
        print("yes")
        users = User.query.filter_by(username=search).first()
        if users:
            return redirect(url_for("profile/<search>"))
       
    


@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
    
    form = PostForm()
    posts = Post.query.all()
    user_like_id = []
    if current_user.is_authenticated:
        
        user_like =Like.query.filter(Like.author==current_user).all()
        for like in user_like:
            user_like_id.append(like.post_id)
    
   
    if request.method=="POST":
        

        try:
            content = request.form["content"]
            post_id = request.form["post"]
            com =Comment(content=content,author=current_user,post=posts[int(post_id)-1])
        
            db.session.add(com)
            db.session.commit()
        except KeyError:
            pass

        try:
            l = request.form["like_box"]
            post_id = request.form["post"]
            query = Like.query.filter(Like.author==current_user, Like.post==posts[int(post_id)-1]).first()
            if query:
                Like.query.filter(Like.author==current_user, Like.post==posts[int(post_id)-1]).delete()
                db.session.commit()
                user_like_id = []
                user_like =Like.query.filter(Like.author==current_user).all()
                for like in user_like:
                    user_like_id.append(like.post_id)
            else:
                like = Like(author=current_user,post=posts[int(post_id)-1])     
                db.session.add(like)
                db.session.commit()
                user_like_id = []
                user_like =Like.query.filter(Like.author==current_user).all()
                for like in user_like:
                    user_like_id.append(like.post_id)
        except:
            pass
        
    

           
                
    
            
            
    
    return render_template("user.html",posts=posts,form=form,user_like_id=user_like_id)

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for("home"))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username= form.username.data, email= form.email.data, password=hashed_password )
        db.session.add(user)
        db.session.commit()
        flash("Your Account ha been craeted, you can now log in!", "success")
        return redirect(url_for("login"))
    return render_template("register.html",form = form)

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for("home"))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login Successful!","success")
            next_page = request.args.get("next ")
            return redirect("next_page") if next_page else redirect(url_for("home"))
        else:

            flash("Login Unsuccesful. Please check username and password","danger")

    return render_template("login.html",form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture,size=(125,125)):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path,"static/assets",picture_fn)

    output_size = size
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    
    return picture_fn

@app.route("/account",methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            
            picture_file= save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username= form.username.data
        current_user.email= form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash("your account has been updated","success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    image_file= url_for('static',filename='assets/'+ current_user.image_file)
    return render_template("edit_account.html",image_file= image_file, form =form)



@app.route("/post",methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        
        if form.picture.data:
            
            test= save_picture(form.picture.data,size=(1000,1000))
            
        
        
        flash("Your Post has been created!","success")
        post = Post(title=form.title.data,content=form.content.data,author=current_user,img=test,priv=form.priv.data)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_post.html",form=form)





    


@app.route("/profile/<user>",methods=["GET","POST"])
def profile(user):
    name = User.query.filter_by(username=user).first()
    
    image_file= url_for('static',filename='assets/'+ name.image_file)
    username = name.username
    email = name.email
    bio = name.bio

    return render_template("profile.html",image_file=image_file,username=username,email=email,bio=bio,posts=name.posts)


@app.route("/test",methods=["GET","POST"])
def test():
    
       
    coms = Like.query.all()
    return render_template("post.html",coms=coms)