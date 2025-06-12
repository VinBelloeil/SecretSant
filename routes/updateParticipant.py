from flask import Blueprint, render_template, request, redirect, flash
from services.serviceParticipant import clear_exclusions, update_participant
from database import db, Participant 

updateParticipant_bp = Blueprint('update', __name__)

@updateParticipant_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        try:
            update_participant(id, request.form['name'])
        except ValueError as e:
            flash(str(e), "danger")
        return redirect('/participant')
    else:
        participant_update = Participant.query.get(id)
        groupe = Participant.query.all()
        exclusions = [e.excluded_id for e in participant_update.exclusions]
        return render_template('/update_participant.html', participant=participant_update, groupe=groupe, exclusions=exclusions)

@updateParticipant_bp.route('/clear/<int:id>', methods=['POST'])
def clearExclusions(id):
    clear_exclusions(id)
    return redirect(f'/update/{id}')
