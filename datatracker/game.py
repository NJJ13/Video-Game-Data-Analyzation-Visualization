from flask import Blueprint, render_template, request, flash, redirect, url_for

import requests, json
from types import SimpleNamespace

from .models.game import Game

bp = Blueprint('games', __name__)


@bp.route('/games', methods=('GET', 'POST'))
def display_games():
    if request.method == 'GET':
        return render_template('games/index.html')
    else:
        api_result = requests.get('https://api.dccresource.com/api/games')
        games = api_result.json()
        chosen_game = request.form['title']
        search_results = []
        for title in games:
            if title['name'].lower() == chosen_game.lower():
                search_results.append(title)

            if title['name'].lower().find(chosen_game) > -1:
                search_results.append(title)
        return render_template('games/index.html', title=search_results)



