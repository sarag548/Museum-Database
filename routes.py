import os
import secrets
from sqlalchemy import func, and_, or_
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
#from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DeptForm, DeptUpdateForm, AssignUpdateForm
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ArtistUpdateForm, ArtworkUpdateForm, DateSearchForm
from flaskDemo.models import User, Post, Artist, Art_Mediums, Art_Work, Era, Medium
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    mylist = ["Artists","Artwork","Eras","Mediums"]
    return render_template('home2.html', outString = mylist)
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/artworks')
def Artwork():
    artworks = result = Art_Work.query.join(Art_Mediums, Art_Work.RefNumberID == Art_Mediums.RefNumberID).add_columns(Art_Work.ArtTitle, Art_Work.RefNumberID) \
                    .join(Medium, Medium.MediumID ==  Art_Mediums.MediumID).add_columns(Medium.Medium, Medium.MediumID) \
                    .join(Artist, Art_Work.ArtistID == Artist.ArtistID).add_columns(Artist.ArtistFName, Artist.ArtistLName, Artist.ArtistID) \
                    .join(Era, Art_Work.EraID == Era.EraID).add_columns(Era.EraStartDate, Era.EraEndDate) \
                    .order_by(Art_Work.ArtistID).group_by(Art_Work.ArtTitle) #group by makes titles distinct
    return render_template('artworks_home.html', outString = artworks)

@app.route('/artworks/<refNum>/<ArtTitle>')
def artwork_page(refNum, ArtTitle):
    artworks = Art_Work.query.join(Art_Mediums, Art_Work.RefNumberID == Art_Mediums.RefNumberID).add_columns(Art_Work.ArtTitle, Art_Work.RefNumberID) \
                    .join(Medium, Medium.MediumID ==  Art_Mediums.MediumID).add_columns(Medium.Medium, Medium.MediumID) \
                    .join(Artist, Art_Work.ArtistID == Artist.ArtistID).add_columns(Artist.ArtistFName, Artist.ArtistLName, Artist.ArtistID) \
                    .join(Era, Art_Work.EraID == Era.EraID).add_columns(Era.EraStartDate, Era.EraEndDate) \
                    .filter(and_(Art_Work.ArtTitle.like(ArtTitle), Art_Work.RefNumberID.like(refNum)))
    return render_template('artworks_page.html', outString=artworks, title=ArtTitle, num=refNum)

@app.route('/mediums')
def Mediums():
    mediums = Medium.query.all()
    return render_template('mediums_home.html', outString = mediums)

@app.route('/eras')
def Eras():
    eras = Era.query.all()
    return render_template('eras.html', outString = eras)

@app.route('/artists')
def Artists():
    artists = Artist.query.all()
    return render_template('artist_home.html', outString = artists)

@app.route('/artists/<firstName>/<lastName>')
def artist_search(firstName, lastName):
    artist = Art_Work.query.join(Art_Mediums, Art_Work.RefNumberID == Art_Mediums.RefNumberID).add_columns(Art_Work.ArtTitle, Art_Work.RefNumberID) \
                    .join(Medium, Medium.MediumID ==  Art_Mediums.MediumID).add_columns(Medium.Medium, Medium.MediumID) \
                    .join(Artist, Art_Work.ArtistID == Artist.ArtistID).add_columns(Artist.ArtistFName, Artist.ArtistLName, Artist.ArtistID) \
                    .join(Era, Art_Work.EraID == Era.EraID).add_columns(Era.EraStartDate, Era.EraEndDate) \
                    .filter(Artist.ArtistFName.like(firstName), Artist.ArtistLName.like(lastName)).order_by(Art_Work.ArtTitle) \
                    .group_by(Art_Work.RefNumberID)
    artCount = Artist.query.join(Art_Work, Artist.ArtistID == Art_Work.ArtistID).filter(Artist.ArtistFName.like(firstName), Artist.ArtistLName.like(lastName)).count()
    return render_template('searchArtist.html', outString = artist, counter = artCount)

@app.route('/mediums/<desc>')
def mediums_search(desc):
    mediums = Art_Work.query.join(Art_Mediums, Art_Work.RefNumberID == Art_Mediums.RefNumberID).add_columns(Art_Work.ArtTitle, Art_Work.RefNumberID) \
                    .join(Medium, Medium.MediumID ==  Art_Mediums.MediumID).add_columns(Medium.Medium, Medium.MediumID) \
                    .join(Artist, Art_Work.ArtistID == Artist.ArtistID).add_columns(Artist.ArtistFName, Artist.ArtistLName, Artist.ArtistID) \
                    .join(Era, Art_Work.EraID == Era.EraID).add_columns(Era.EraStartDate, Era.EraEndDate) \
                    .filter(Medium.Medium.like(desc)).order_by(Art_Work.ArtTitle)
    return render_template('searchMedium.html', outString = mediums)

@app.route('/eras/<start>/<end>')
def era_search(start, end):
    eras = Art_Work.query.join(Art_Mediums, Art_Work.RefNumberID == Art_Mediums.RefNumberID).add_columns(Art_Work.ArtTitle, Art_Work.RefNumberID) \
                    .join(Medium, Medium.MediumID ==  Art_Mediums.MediumID).add_columns(Medium.Medium, Medium.MediumID) \
                    .join(Artist, Art_Work.ArtistID == Artist.ArtistID).add_columns(Artist.ArtistFName, Artist.ArtistLName, Artist.ArtistID) \
                    .join(Era, Art_Work.EraID == Era.EraID).add_columns(Era.EraStartDate, Era.EraEndDate) \
                    .filter(Era.EraStartDate.like(start), Era.EraEndDate.like(end)) \
                    .group_by(Art_Work.RefNumberID)
                        #could also change filter condition to where it returns artworks that were made within the same time instead of made at exact time
    return render_template('search.html', outString = eras)


@app.route('/new/artist', methods=['GET', 'POST'])
@login_required
def new_artist():
    form = ArtistUpdateForm()
    if form.validate_on_submit():
        artist = Artist(ArtistFName=form.fname.data, ArtistLName=form.lname.data)
        db.session.add(artist)
        db.session.commit()
        flash('Cool! This artist has now been archived.', 'success')
        return redirect(url_for('home'))
    return render_template('create_artist.html', title='New Artist', form=form, legend='New Artist')

@app.route('/eras/search', methods=['GET', 'POST'])
def date_search():
    form = DateSearchForm()
    if form.validate_on_submit():
        range_one = form.start.data
        range_two = form.end.data
        artworks = Art_Work.query.join(Art_Mediums, Art_Work.RefNumberID == Art_Mediums.RefNumberID).add_columns(Art_Work.ArtTitle, Art_Work.RefNumberID) \
                            .join(Medium, Medium.MediumID ==  Art_Mediums.MediumID).add_columns(Medium.Medium, Medium.MediumID) \
                            .join(Artist, Art_Work.ArtistID == Artist.ArtistID).add_columns(Artist.ArtistFName, Artist.ArtistLName, Artist.ArtistID) \
                            .join(Era, Art_Work.EraID == Era.EraID).add_columns(Era.EraStartDate, Era.EraEndDate) \
                            .filter(and_(Era.EraStartDate > range_one, Era.EraEndDate < range_two)).group_by(Art_Work.ArtTitle).order_by(Era.EraStartDate)
        return render_template('search.html', outString= artworks)
    return render_template('date_search.html', form=form, legend='Search by Date')

@app.route('/artworks/<refNum>/<ArtTitle>/delete', methods=['POST'])
@login_required
def delete_artwork(refNum, ArtTitle):

    artwork = Art_Work.query.get_or_404(refNum) #should search by ID and not name
    artist = Art_Work.query.join(Art_Mediums, Art_Work.RefNumberID == Art_Mediums.RefNumberID).add_columns(Art_Work.ArtTitle, Art_Work.RefNumberID) \
                    .join(Medium, Medium.MediumID ==  Art_Mediums.MediumID).add_columns(Medium.Medium, Medium.MediumID) \
                    .join(Artist, Art_Work.ArtistID == Artist.ArtistID).add_columns(Artist.ArtistFName, Artist.ArtistLName, Artist.ArtistID) \
                    .join(Era, Art_Work.EraID == Era.EraID).add_columns(Era.EraStartDate, Era.EraEndDate) \
                    .filter(Art_Work.ArtTitle.like(ArtTitle), Art_Work.RefNumberID.like(refNum)).order_by(Art_Work.ArtTitle)
    ids = []
    for row in artist:
        ids.append(row.MediumID) #in artmediums grab all the mediumids attached to this artwork
    for i in range(len(ids)):
        mediumID = ids[i]
        artmedium = Art_Mediums.query.get_or_404([refNum, mediumID]) #get the references in artmediums
        db.session.delete(artmedium) #delete those references

    db.session.delete(artwork)
    db.session.commit()
    flash('Artwork has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/artwork/<refNum>/<ArtTitle>/update', methods=['GET', 'POST'])
@login_required
def update_artwork(refNum, ArtTitle):
    artwork = Art_Work.query.get_or_404(refNum) #is returning a 404, should look up by refNum
    currentArt = artwork.ArtTitle
    currentEraID = artwork.EraID
    form = ArtworkUpdateForm()
    if form.validate_on_submit():
        artwork.EraID = form.newEra.data
        db.session.commit()
        flash('Artwork has been updated!', 'success')
        return redirect(url_for('artwork_page', ArtTitle=ArtTitle, refNum=refNum))
    elif request.method =='GET':
        form.newEra.data = currentEraID
    return render_template('update_artwork.html', form=form, legend="Update Artwork", artTitle=currentArt)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
