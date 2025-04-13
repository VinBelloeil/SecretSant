from database import db, Assignment, Draw
from random import shuffle

def draw(participants):
    if len(participants) < 2:
        raise ValueError("You need at least 2 participants.")
    
    exclusions_map = {
        p.id: {ex.excluded_id for ex in p.exclusions} | {p.id} for p in participants
    }
    
    current_attempt = 0
    max_attempt = 100
    givers = participants[:]

    while current_attempt < max_attempt:
        current_attempt += 1
        receivers = participants[:]
        shuffle(receivers)
    
        valid = True    
        for i in range(len(givers)):
            giver = givers[i]
            receiver = receivers[i]
    
            if receiver.id in exclusions_map[giver.id]:
                valid = False
                break

        if valid:
            return assignEveryGift(givers, receivers)
    
    raise ValueError(f"No valid draw after {max_attempt} attempts.")


def assignEveryGift(givers, receivers):
    drawInstance = Draw()
    db.session.add(drawInstance)
    db.session.commit()

    try:
        for i in range(len(givers)):
            choice = Assignment(draw_id=drawInstance.id, giver_id=givers[i].id, receiver_id=receivers[i].id)
            db.session.add(choice)
        db.session.commit()
        return drawInstance
    
    except Exception as e:
        db.session.rollback()
        print(f"Error assigning gifts: {e}")
        raise ValueError(f"Error assigning gifts: {e}")
    