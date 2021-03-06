"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash,session,abort
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignUpForm
from models import UserProfile
from werkzeug.security import check_password_hash
from forms import UploadForm
from werkzeug.utils import secure_filename
import os

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
@app.route('/recipe')
def recipe():
    """Render website's recipe page."""
    return render_template('recipe.html')    


@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Foodies")


@app.route('/secure-page')
@login_required
def secure_page():
    """Render a secure page on our website that only logged in users can access."""
    return render_template('secure_page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form= SignUpForm()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if user is already logged in, just redirect them to our secure page
        # or some other page like a dashboard
        return redirect(url_for('secure_page'))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    # Login and validate the user.
    if request.method == 'POST' and form.validate_on_submit():
        # Query our database to see if the username and password entered
        # match a user that is in the database.
        username = form.username.data
        password = form.password.data

        # user = UserProfile.query.filter_by(username=username, password=password)\
        # .first()
        # or
        user = UserProfile.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True

            # If the user is not blank, meaning if a user was actually found,
            # then login the user and create the user session.
            # user should be an instance of your `User` class
            login_user(user, remember=remember_me)

            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    # if not session.get('logged_in'):
    #     abort(401)

    # Instantiate your form class
    img = UploadForm()
    # Validate file upload on submit
    if request.method == 'POST' and img.validate_on_submit():
        # Get file data and save to your uploads folder
        #img_data = request.files['img_data']
        img_data = img.image.data
        description = img.description.data
        filename = secure_filename(img_data.filename)
        img_data.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        flash('File Saved', 'success')
        return redirect(url_for('home'))

    return render_template('upload.html', form = img)

@app.route('/gallery')
#@login_required
def gallery():
    #displays users' pictures
    return render_template('t.html', images = get_uploaded_images())

def get_uploaded_images():
	rootdir = os.getcwd()
	
	images = []

	for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
		for file in files:
		    name, ext = os.path.splitext(file)
		    if ((ext == '.jpg') or (ext == '.jpeg') or (ext == '.png')):
		        images.append(file)
	return images

########################################################

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
		        images.append(file)
                getattr(form, field).label.text,
                error
            ), 'danger')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
