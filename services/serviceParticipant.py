from database import db, Participant, Exclusion

def add_participant(name):
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()

def delete_participant(id):
    participant_delete = Participant.query.get_or_404(id)
    db.session.delete(participant_delete)
    db.session.commit()

def update_participant(id, new_name):
    participant_update = Participant.query.get_or_404(id)
    participant_update.name = new_name
    db.session.commit()

def clear_exclusions(id):
    exclusion_list = Exclusion.query.filter_by(participant_id=id).all()
    for exclusion in exclusion_list:
        db.session.delete(exclusion)
    db.session.commit()

def exclude_participant(id, idToExclude):
    exclusion = Exclusion(participant_id=id, excluded_id=idToExclude)
    db.session.add(exclusion)
    db.session.commit()

def include_participant(id, idToInclude):
    exclusion = Exclusion.query.filter_by(participant_id=id, excluded_id=idToInclude).first()
    if exclusion:
        db.session.delete(exclusion)
        db.session.commit()