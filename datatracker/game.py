from flask import Blueprint, render_template

import requests, json
from types import SimpleNamespace

from .models.game import Game

bp = Blueprint('games', __name__)


@bp.route('/games', methods=['GET'])
def display_games():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    return render_template('games/index.html', games=games)

