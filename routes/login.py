from flask import Blueprint, request,session,flash,render_template,redirect,url_for
from database import db, Participant
from werkzeug.security import generate_password_hash, check_password_hash

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        participant = Participant.query.filter_by(email=email).first()
        
        if participant and check_password_hash(participant.password_hash, password):
            session['participant_id'] = participant.id
            session['user'] = participant.name 
            flash('Login successful!', 'success')
            return redirect(url_for('participant.participant')) 
        else:
            flash('Login failed. Check your email and password.', 'danger')
    
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('participant_id', None)
    session.pop('user', None)  # Remove the user variable from the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login.login'))


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('login.register'))

        existing_user = Participant.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'error')
            return redirect(url_for('login.register'))

        new_participant = Participant(name=name, email=email)
        new_participant.set_password(password)
        db.session.add(new_participant)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login.login'))

    return render_template('register.html')
