from flask import Blueprint, render_template, request, redirect
from services.serviceParticipant import add_participant, delete_participant
from database import db, Participant 

participant_bp = Blueprint('participant', __name__)

@participant_bp.route('/')
@participant_bp.route('/participant', methods=['POST', 'GET'])
def participant():
    if request.method == 'POST':
        name_new_participant = request.form['name']
        add_participant(name_new_participant)
        return redirect('/participant')
    else:
        participants = Participant.query.all()
        return render_template('participants.html', participants=participants)

@participant_bp.route('/delete/<int:id>')
def supprimer(id):
    delete_participant(id)
    return redirect('/participant')
