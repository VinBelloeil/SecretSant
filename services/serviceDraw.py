from database import db, Assignment, Draw
from random import sample
from sqlalchemy.exc import SQLAlchemyError

def draw(participants):
    if len(participants) < 2:
        raise ValueError("You need at least 2 participants.")

    # Map des exclusions : chaque participant ne peut pas tirer ses exclusions ou lui-même
    exclusions_map = {
        p.id: {ex.excluded_id for ex in p.exclusions} | {p.id}
        for p in participants
    }

    givers = [p.id for p in participants]
    receivers = [p.id for p in participants]
    assignment = {}

    def backtrack(index=0):
        if index == len(givers):
            return True  # Fin de la récursion avec succès

        giver = givers[index]
        possible_receivers = [r for r in receivers if r not in exclusions_map[giver]]

        for receiver in sample(possible_receivers, len(possible_receivers)):  # randomize
            assignment[giver] = receiver
            receivers.remove(receiver)
            if backtrack(index + 1):
                return True
            receivers.append(receiver)
            del assignment[giver]

        return False  # Aucun tirage possible pour ce donneur

    if not backtrack():
        raise ValueError("No valid draw found.")

    return assignEveryGift(participants, assignment)


def assignEveryGift(participants, assignment):
    draw_instance = Draw()
    db.session.add(draw_instance)
    db.session.commit()

    try:
        for giver in participants:
            receiver_id = assignment[giver.id]
            choice = Assignment(
                draw_id=draw_instance.id,
                giver_id=giver.id,
                receiver_id=receiver_id
            )
            db.session.add(choice)
        db.session.commit()
        return draw_instance

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error assigning gifts: {e}")
        raise ValueError("An error occurred while saving the draw to the database.")

    