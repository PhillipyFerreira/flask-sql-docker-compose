# -*- coding: utf-8 -*-

"""Users views."""
import logging
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

from flask import (Blueprint, abort, flash, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_user, logout_user

from database import db
from users.models import User

from .decorators import requires_login
from .forms import (EmailForm, LoginForm, PasswordForm,
                    SettingsForm, SignUpForm)

try:
    import run_celery
except ImportError:
    # migrations hack
    pass


users = Blueprint('users', __name__)
login_url = 'users.login'

@users.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.query(User).get(form.user.id)
        
        if user.check_password(form.password.data):
            login_user(user)
            session['client_id'] = user.id
            return redirect(request.args.get('next') or url_for('default_index'))
        else:
            logging.debug("Login failed.")
            flash(u"Login failed.", 'error')
    
    return redirect(url_for(login_url))  # Redireciona para a página inicial em caso de falha no login

@users.route('/login', methods=['GET'])
def login_form():
    form = LoginForm()
    return render_template('users/login.html', form=form)


@users.route('/logout')
@requires_login
def logout():
    logout_user()
    session.pop('client_id', None)
    flash(u"You were logged out", 'success')
    return redirect(url_for(login_url))


@users.route('/signup', methods=('POST'))
def signup():
    form = SignUpForm()
    session.pop('client_id', None)
    if form.validate_on_submit():
        logging.debug("Email: {0}".format(form.email.data))
        check_user = User.query.filter_by(email=form.email.data).first()
        print(check_user)
        if check_user:
            logging.debug(
                "Email {0} already exist in the database.".format(
                    form.email.data))
            msg = u"""
                User with email {0} already exist.
            """
            flash(msg, 'error')
            return redirect(url_for('users.signup'))
        user = User(form.email.data, form.password.data)
        user.email = form.email.data
        user.set_password(form.password.data)
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        elif request.headers.get("X-Real-IP"):
            ip = request.headers.get("X-Real-IP")
        else:
            ip = request.remote_addr
        user.first_ip = ip
        db.session.add(user)
        # Now we'll send the email confirmation link
        try:
            ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
            token = ts.dumps(user.email, salt='email-confirm-key')
            logging.debug("Confirm token: {0}".format(token))
        except Exception as e:
            logging.error(e)
            abort(404)
        subject = u"Confirm your email"
        confirm_url = url_for(
            'users.confirm_email', token=token, _external=True)
        html = render_template(
            'emails/confirmation.html', confirm_url=confirm_url)
        run_celery.send_email.apply_async(
            (user.email, subject, html)
        )
        msg = u"""
            Account was successfully created.
            Check your email to confirm account.
        """
        logging.debug("New account was successfully created.")
        flash(msg, 'success')
        db.session.commit()
    return redirect(url_for(login_url))


@users.route('/signup', methods=('GET'))
def signup():
    form = SignUpForm()
    session.pop('client_id', None)
    return render_template('users/signup.html', form=form)

@users.route('/settings', methods=('POST'))
@requires_login
def settings():
    form = SettingsForm()
    user = db.session.query(User).get(current_user.get_id())

    if not user:
        abort(404)

    if form.validate_on_submit():
        if user.check_password(form.password.data):
            if not is_email_unique(form.email.data, user) or not is_phone_unique(form.phone.data, user):
                return redirect_with_error("This email or phone already exist.", 'error')

            update_user_information(user, form)
            return redirect_with_success("Your changes have been saved.")

        else:
            return redirect_with_error("Please, check password again.", 'error')
    else:
        populate_form_with_user_data(form, user)

    return render_template('users/settings.html', form=form)

@users.route('/settings', methods=('GET'))
@requires_login
def settings():
    form = SettingsForm()
    user = db.session.query(User).get(current_user.get_id())

    if not user:
        abort(404)

    return render_template('users/settings.html', form=form)

def is_email_unique(email, user):
    return email != user.email and not User.query.filter_by(email=email).scalar()

def is_phone_unique(phone, user):
    return phone != user.phone and User.query.filter_by(phone=phone).scalar()

def update_user_information(user, form):
    user.email = form.email.data
    user.phone = form.phone.data
    new_password = form.new_password.data
    confirm = form.confirm.data

    if new_password and confirm and new_password == confirm:
        user.set_password(new_password)
        db.session.add(user)
        db.session.commit()

def populate_form_with_user_data(form, user):
    form.email.data = user.email
    form.phone.data = user.phone

def redirect_with_error(message, category='error'):
    flash(message, category)
    return redirect(url_for('users.settings'))

def redirect_with_success(message, category='success'):
    flash(message, category)
    return redirect(url_for('users.settings'))



@users.route('/confirm/<token>')
def confirm_email(token):
    try:
        ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except Exception as e:
        logging.error(e)
        abort(404)
    logging.debug("Token: {0} email: {1}".format(token, email))
    user = User.query.filter_by(email=email).first_or_404()
    user.active = True
    user.confirmed_date = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    msg = u"""
        Thanks! Your email address was confirmed.
        Your account is active now. Please, login.
    """
    flash(msg, 'success')
    logging.debug("Account {0} is active now.".format(email))
    return redirect(url_for(login_url))


@users.route('/reset', methods=["POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        logging.debug(
            "Password reset request from {0}".format(
                user.email))
        subject = "Password reset requested"
        # Here we use the URLSafeTimedSerializer we created in `util` at the
        # beginning of the chapter
        try:
            ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
            token = ts.dumps(user.email, salt='recover-key')
        except Exception as e:
            logging.error(e)
            abort(404)
        recover_url = url_for(
            'users.reset_with_token',
            token=token,
            _external=True)
        html = render_template(
            'emails/recover.html',
            recover_url=recover_url)
        run_celery.send_email.apply_async(
            (user.email, subject, html)
        )
        msg = u"""
            Please, check your email.
        """
        flash(msg, 'error')
        return redirect(url_for(login_url))


@users.route('/reset', methods=["GET"])
def reset():
    form = EmailForm()
    return render_template('users/reset.html', form=form)

@users.route('/reset/<token>', methods=["POST"])
def reset_with_token(token):
    try:
        ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except Exception as e:
        logging.error(e)
        abort(404)
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for(login_url))

@users.route('/reset/<token>', methods=["GET"])
def reset_with_token(token):
    form = PasswordForm()
    return render_template(
        'users/reset_with_token.html', form=form, token=token)