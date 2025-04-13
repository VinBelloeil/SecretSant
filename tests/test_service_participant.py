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
            add_participant('Alice')  
            self.assertEqual(Participant.query.count(), 1)  # 1 participant 
            participant = Participant.query.first()
            self.assertEqual(participant.name, 'Alice')

    def test_delete_participant(self):
        with app.app_context():
            add_participant('Bob')
            participant = Participant.query.first()
            add_participant('Charlie')  # add 2 participants
            self.assertEqual(Participant.query.count(), 2)
            delete_participant(participant.id)
            self.assertEqual(Participant.query.count(), 1)  # 1 remaining participant
            self.assertEqual(Participant.query.first().name, 'Charlie')

    def test_update_participant(self):
        with app.app_context():
            add_participant('Alice')
            participant = Participant.query.first()
            self.assertEqual(participant.name, 'Alice')  # Initial name
            update_participant(participant.id, 'Alicia')
            participant = Participant.query.first()
            self.assertEqual(participant.name, 'Alicia')

    def test_clear_exclusions(self):
        with app.app_context():
            add_participant('Alice')
            add_participant('Bob')
            alice = Participant.query.filter_by(name='Alice').first()
            bob = Participant.query.filter_by(name='Bob').first()
            exclude_participant(alice.id, bob.id)
            self.assertEqual(Exclusion.query.count(), 1)
            clear_exclusions(alice.id)
            self.assertEqual(Exclusion.query.count(), 0)  # 0 exclusion after cleaning

    def test_exclude_participant(self):
        with app.app_context():
            add_participant('Alice')
            add_participant('Bob')
            alice = Participant.query.filter_by(name='Alice').first()
            bob = Participant.query.filter_by(name='Bob').first()
            self.assertEqual(Exclusion.query.count(), 0)
            exclude_participant(alice.id, bob.id)
            exclusion = Exclusion.query.first()
            self.assertEqual(exclusion.participant_id, alice.id)
            self.assertEqual(exclusion.excluded_id, bob.id)
            self.assertEqual(Exclusion.query.count(), 1)

    def test_include_participant(self):
        with app.app_context():
            add_participant('Alice')
            add_participant('Bob')
            alice = Participant.query.filter_by(name='Alice').first()
            bob = Participant.query.filter_by(name='Bob').first()
            exclude_participant(alice.id, bob.id)
            self.assertEqual(Exclusion.query.count(), 1)  # 1 Exclusion before
            include_participant(alice.id, bob.id)
            self.assertEqual(Exclusion.query.count(), 0) # 0 Exclusion after

if __name__ == '__main__':
    unittest.main()
