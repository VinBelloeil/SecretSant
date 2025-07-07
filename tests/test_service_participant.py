import unittest
from app import app, db
from services.serviceParticipant import *
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

    def test_add_participant(self):
        with app.app_context():
            self.assertEqual(Participant.query.count(), 0)  # 0 participant

            add_participant('Alice','alice@alice.com') 

            self.assertEqual(Participant.query.count(), 1)  # 1 participant 
            participant = Participant.query.first()
            self.assertEqual(participant.name, 'Alice')

    def test_add_blank_name(self):
        with self.assertRaises(ValueError) as context:
            add_participant("   ","")
            assert "cannot be empty" in str(context.value).lower()

    def test_add_duplicate_name(self):
        with app.app_context():
            bob = Participant(name='Bob',email = "bob@bob.com")
            db.session.add(bob)
            db.session.commit()
    
            with self.assertRaises(ValueError) as context:
                add_participant("bob","bob@bob.com")  # insensible à la casse

            self.assertIn("already exists", str(context.exception).lower())

    def test_delete_participant(self):
        with app.app_context():
            bob = Participant(name='Bob',email = "bob@bob.com")
            charlie = Participant(name='Charlie',email= "charlie@charlie.com")
            db.session.add(bob)
            db.session.add(charlie)
            db.session.commit() # add 2 participants
            self.assertEqual(Participant.query.count(), 2)

            delete_participant(bob.id)

            self.assertEqual(Participant.query.count(), 1)  # 1 remaining participant
            self.assertEqual(Participant.query.first().name, 'Charlie')

    def test_update_participant(self):
        with app.app_context():
            alice = Participant(name='Alice',email = "alice@alice.com")
            db.session.add(alice)
            db.session.commit()
            self.assertEqual(alice.name, 'Alice')  # Initial name

            update_participant(alice.id, 'Alicia')

            participant = Participant.query.first()
            self.assertEqual(participant.name, 'Alicia')

    def test_update_with_existing_name(self):
        with app.app_context():
            alice = Participant(name='Alice',email = "alice@alice.com")
            bob = Participant(name='Bob',email = "bob@bob.com")
            db.session.add(alice)
            db.session.add(bob)
            db.session.commit()

            with self.assertRaises(ValueError) as context:
                update_participant(bob.id,"alice")  # insensible à la casse

            self.assertIn("already exists", str(context.exception).lower())

    def test_clear_exclusions(self):
        with app.app_context():
            alice = Participant(name='Alice',email = "alice@alice.com")
            bob = Participant(name='Bob',email = "bob@bob.com")
            db.session.add(alice)
            db.session.add(bob)
            db.session.commit()
            exclusion = Exclusion(participant_id=alice.id, excluded_id=bob.id)
            db.session.add(exclusion)
            db.session.commit()

            clear_exclusions(alice.id)

            self.assertEqual(Exclusion.query.count(), 0)  # 0 exclusion after cleaning

    def test_exclude_participant(self):
        with app.app_context():
            alice = Participant(name='Alice',email = "alice@alice.com")
            bob = Participant(name='Bob',email = "bob@bob.com")
            db.session.add(alice)
            db.session.add(bob)
            db.session.commit()
            self.assertEqual(Exclusion.query.count(), 0)

            exclude_participant(alice.id, bob.id)

            exclusion = Exclusion.query.first()
            self.assertEqual(exclusion.participant_id, alice.id)
            self.assertEqual(exclusion.excluded_id, bob.id)
            self.assertEqual(Exclusion.query.count(), 1)

    def test_include_participant(self):
        with app.app_context():
            alice = Participant(name='Alice',email = "alice@alice.com")
            bob = Participant(name='Bob',email = "bob@bob.com")
            db.session.add(alice)
            db.session.add(bob)
            db.session.commit()
            exclusion = Exclusion(participant_id=alice.id, excluded_id=bob.id)
            db.session.add(exclusion)
            db.session.commit()
            self.assertEqual(Exclusion.query.count(), 1)  # 1 Exclusion before

            include_participant(alice.id, bob.id)

            self.assertEqual(Exclusion.query.count(), 0) # 0 Exclusion after

if __name__ == '__main__':
    unittest.main()
