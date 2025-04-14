from flask import Blueprint, redirect
from services.serviceParticipant import exclude_participant, include_participant

exclusion_bp = Blueprint('exclusion', __name__)

@exclusion_bp.route('/exclusion/<int:id>/<int:idToExclude>', methods=['POST'])
def exclude(id, idToExclude):
    exclude_participant(id, idToExclude)
    return redirect(f'/update/{id}')

@exclusion_bp.route('/inclusion/<int:id>/<int:idToInclude>', methods=['POST'])
def include(id, idToInclude):
    include_participant(id, idToInclude)
    return redirect(f'/update/{id}')
