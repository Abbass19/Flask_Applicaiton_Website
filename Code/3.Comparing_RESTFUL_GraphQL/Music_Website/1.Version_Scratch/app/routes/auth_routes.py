from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from ..models import *

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
@auth.route('/Signup', methods=['GET', 'POST'])
@auth.route('/signup/', methods=['GET', 'POST'])
@auth.route('/Signup/', methods=['GET', 'POST'])


def signup():
    if request.method == 'POST':
        # Add sign up logic here
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        company = request.form.get('company')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        postal_code = request.form.get('postalCode')

        if not first_name or not last_name or not email or not password1 or not password2:
            flash('Please fill out all required fields.', category='error')
            return render_template('signup.html')

        if password1 != password2:
            flash('Passwords do not match.', category='error')
            return render_template('signup.html')

        existing_user = Customer.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', category='error')
            return render_template('signup.html')

        # Hash password before saving (assuming Customer has a password field)
        # hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')

        #Creating new Customer
        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company=company,
            address=address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            fax=password2  # You must add this field in your model
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Account created successfully! Please log in.', category='success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/Login', methods=['GET', 'POST'])
@auth.route('/login/', methods=['GET', 'POST'])
@auth.route('/Login/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Customer.query.filter_by(email=email).first()
        if not user:
            flash('Email not found. Please try again.', category='error')
            return redirect(url_for('auth.login'))
        # assuming your Customer model has a 'password' field storing the hashed password
        if not (user.fax == password):
            flash('Incorrect password. Please try again.', category='error')
            return redirect(url_for('auth.login'))

        # TODO: Log the user in (using flask-login or session)
        # For example:
        # login_user(user)

        flash('Logged in successfully!', category='success')
        session['user_id'] = user.customer_id  # store only user ID
        return redirect(url_for('main.home'))  # redirect to your main page

    if request.method =='GET':
        if session.get('user_id') :
            flash("You are Already Signed In ", category='succeed')
            return redirect(url_for('main.home'))
    return render_template('login.html')



