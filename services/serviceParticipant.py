from database import db, Participant, Exclusion

def add_participant(name,email):
    clean_name = validate_participant_name(name)
    new_participant = Participant(name=clean_name,email=email)
    db.session.add(new_participant)
    db.session.commit()

def update_participant(id, new_name, new_email=None):
    participant_update = Participant.query.get_or_404(id)
    
    clean_name = validate_participant_name(new_name, exclude_id=id)
    participant_update.name = clean_name

    if new_email is not None:
        participant_update.email = new_email
    
    db.session.commit()

def validate_participant_name(name, exclude_id=None):
    clean_name = name.strip()

    if not clean_name:
        raise ValueError("Participant name cannot be empty.")

    query = Participant.query.filter(
        db.func.lower(Participant.name) == clean_name.lower()
    )

    if exclude_id is not None:
        query = query.filter(Participant.id != exclude_id)

    if query.first():
        raise ValueError(f"A participant named '{clean_name}' already exists.")
    
    return clean_name

def delete_participant(id):
    participant_delete = Participant.query.get_or_404(id)
    db.session.delete(participant_delete)
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