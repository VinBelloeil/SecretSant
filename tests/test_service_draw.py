import unittest
from app import app, db
from services.serviceDraw import *
from database import Participant,Exclusion

class TestServices(unittest.TestCase):

    def setUp(self):
        
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
        self.app = app.test_client()
        with app.app_context():
            db.create_all()  

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()  

    def test_draw_with_less_than_two_participants(self):
        with app.app_context():
            # add only 1 participant
            participant = Participant(name='Alice')
            db.session.add(participant)
            db.session.commit()

            with self.assertRaises(ValueError) as context:
                draw([participant])

            self.assertEqual(str(context.exception), "You need at least 2 participants.")

    def test_draw_without_exclusions(self):
        with app.app_context():
            alice = Participant(name='Alice')
            bob = Participant(name='Bob')
            db.session.add(alice)
            db.session.add(bob)
            db.session.commit()

            result = draw([alice, bob])

            self.assertEqual(len(result.assignments), 2) 
            self.assertEqual(result.assignments[0].giver_id, alice.id)
            self.assertEqual(result.assignments[1].giver_id, bob.id)

    def test_draw_with_exclusions(self):
        with app.app_context():
            # Add 3 participants
            alice = Participant(name='Alice')
            bob = Participant(name='Bob')
            charlie = Participant(name='Charlie')
            db.session.add(alice)
            db.session.add(bob)
            db.session.add(charlie)
            db.session.commit()

            # Alice excludes Bob
            alice_exclusion = Exclusion(participant_id=alice.id, excluded_id=bob.id)
            db.session.add(alice_exclusion)
            db.session.commit()

            result = draw([alice, bob, charlie])

            assignments = [(a.giver_id, a.receiver_id) for a in result.assignments]
            self.assertNotIn((alice.id, bob.id), assignments)  # Alice's receiver musn't be Bob

    def test_draw_fail_after_max_attempts(self):
        with app.app_context():
            # Add 3 participants
            alice = Participant(name='Alice')
            bob = Participant(name='Bob')
            charlie = Participant(name='Charlie')
            db.session.add(alice)
            db.session.add(bob)
            db.session.add(charlie)
            db.session.commit()

            # Alice excludes all other participants
            alice_exclusion_1 = Exclusion(participant_id=alice.id, excluded_id=bob.id)
            alice_exclusion_2 = Exclusion(participant_id=alice.id, excluded_id=charlie.id)
            db.session.add(alice_exclusion_1)
            db.session.add(alice_exclusion_2)
            db.session.commit()
            
            with self.assertRaises(ValueError) as context:
                draw([alice, bob, charlie])

            self.assertTrue("No valid draw after 100 attempts." in str(context.exception))

if __name__ == '__main__':
    unittest.main()
