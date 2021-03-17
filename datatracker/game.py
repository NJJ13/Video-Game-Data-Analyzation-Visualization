from flask import Blueprint, render_template, request, flash, redirect, url_for

import requests, json
from types import SimpleNamespace
from pychartjs import BaseChart, ChartType, Color


bp = Blueprint('games', __name__)


@bp.route('/games', methods=['GET'])
def display_games():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    return render_template('games/index.html', games=games)


@bp.route('/platform')
def invest_console():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content)

    class BarChart(BaseChart):

        type = ChartType.Bar

        class Data:
            label = games['platform']
            data = games['globalSales']
            backgroundColor = Color.Blue
    return render_template('games/platform.html')


@bp.route('/games/search', methods=('GET', 'POST'))
def search_games():
    if request.method == 'POST':
        id = request.form['_id']
        error = None

        if not id:
            error = 'You must enter an ID'

        if error is not None:
            flash(error)
        elif request.form['_id'] != "":
            return redirect(url_for('games.game_details', id=id))
        else:
            return render_template('games/search.html', id=id)

    else:
        return render_template('games/search.html', id="")


@bp.route('/games/<id>', methods=['GET'])
def game_details(id):
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    for game in games:
        if game._id == id:
            found_game = game
    return render_template('games/details.html', found_game=found_game)
