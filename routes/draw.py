from flask import Blueprint, render_template
from services.serviceDraw import draw
from database import Draw,Participant

draw_bp = Blueprint('tirage', __name__)

@draw_bp.route('/tirage')
def drawRoute():
    participants = Participant.query.all()
    error_message = None
    try:
        lastDraw = draw(participants)
    except ValueError as e:
        error_message = str(e)
    drawHistory = Draw.query.order_by(Draw.created.desc()).limit(5).all()
    return render_template('/tirage.html', draws=drawHistory, error=error_message)
