from flask import Flask
from database import db
from routes.participant import participant_bp
from routes.draw import draw_bp
from routes.exclusion import exclusion_bp
from routes.updateParticipant import updateParticipant_bp
from routes.login import login_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secretSanta.db'
db.init_app(app)

app.secret_key = 'une_clé_secrète_très_sécurisée'

app.register_blueprint(login_bp)
app.register_blueprint(participant_bp)
app.register_blueprint(draw_bp)
app.register_blueprint(exclusion_bp)
app.register_blueprint(updateParticipant_bp)

if __name__ == '__main__':
    app.run(debug=True)
