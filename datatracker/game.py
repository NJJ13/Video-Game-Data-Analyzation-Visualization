from flask import Blueprint, render_template, request, flash, redirect, url_for

import requests, json
from types import SimpleNamespace

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


@bp.route('/platform')
def total_sales():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    consoles = []
    for game in games:
        if game.year is None:
            continue
        elif game.platform in consoles:
            continue
        elif game.year >= 2013:
            consoles.append(game.platform)

    global_sales_dict = {i: 0 for i in consoles}
    for game in games:
        if game.platform in global_sales_dict:
            global_sales_dict[game.platform] += round(game.globalSales)

    global_sales = list(global_sales_dict.values())

    return render_template('games/platform.html', global_sales_dict=global_sales_dict, labels=consoles,
                           values=global_sales)


@bp.route('/games/<id>', methods=['GET'])
def game_details(id):
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    for game in games:
        if game._id == id:
            found_game = game
    return render_template('games/details.html', found_game=found_game)


@bp.route('/game/<name>', methods=['GET'])
def console_breakdown(name):
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    cross_platform_game = []
    for game in games:
        if game.name == name:
            cross_platform_game.append(game)
    return render_template('games/console_breakdown.html', cross_platform_game=cross_platform_game)

