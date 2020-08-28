from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from my_app import db, photos
from my_app.community.forms import ProfileForm
from my_app.models import Profile, User

community_bp = Blueprint('community', __name__, url_prefix='/community')


@community_bp.route('/')
def index():
    return render_template("community.html")


@community_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('community.update_profile'))
    else:
        return redirect(url_for('community.create_profile'))


@community_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        u = User.query.filter_by(id=current_user.id)
        filename = None
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                filename = photos.save(request.files['photo'])
        p = Profile(country=repr(form.country.data), username=form.username.data, photo=filename, bio=form.bio.data,
                    user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('community.display_profiles', username=p.username))
    return render_template('profile.html', form=form)


@community_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    form = ProfileForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            profile.photo = filename
        profile.country = form.country.data
        profile.bio = form.bio.data
        profile.username = form.username.data
        db.session.commit()
        return redirect(url_for('community.display_profiles', username=profile.username))
    return render_template('profiles.html', form=form)


@community_bp.route('/display_profiles', methods=['POST', 'GET'])
@community_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username=None):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("community.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("No users found.")
        return redirect(url_for("community.index"))
    urls = []
    for result in results:
        url = photos.url(result.photo)
        urls.append(url)
    return render_template('display_profile.html', profiles=zip(results, urls))
