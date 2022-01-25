from flask import Blueprint, render_template, request, flash
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html",  datetime=str(datetime.now().year))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        postal_list = [
            'street_number',
            'route',
            'postal_town',
            'administrative_area_level_2',
            'postal_code'
        ]
        full_address_list = []
        separator = ', '
        for i in postal_list:
            full_address_list.append(request.form.get(i))

        full_address = separator.join(full_address_list)

        if len(email) < 4:
            flash('Email must be greater 3 characters', category='error')
        elif len(full_name) < 4:
            flash('Full Name must be greater than 3 characters', category='error')
        elif password != password_confirm:
            flash('Passwords do not match', category='error')
        elif len(password) < 8:
            flash('Password must be greater than 7 characters', category='error')
        else:
            flash('Account successfully created!', category='success')

    return render_template("register.html",  datetime=str(datetime.now().year))
