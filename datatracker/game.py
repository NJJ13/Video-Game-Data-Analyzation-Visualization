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
def invest_console():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    total = 0
    for game in games:
        if game.platform == "DS":
            total += game.globalSales
    return render_template('games/platform.html', total=total)


@bp.route('/games/<id>', methods=['GET'])
def game_details(id):
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    for game in games:
        if game._id == id:
            found_game = game
    return render_template('games/details.html', found_game=found_game)


@bp.route('/games/<name>', methods=['GET'])
def console_breakdown(name):
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    cross_platform_game = []
    for game in games:
        if game.name == name:
            cross_platform_game.append(game)
    return render_template('games/console_breakdown.html', cross_platform_game=cross_platform_game)


@bp.route('/games/chart_page2')
def genre_stats():
    response = requests.get('https://api.dccresource.com/api/games')
    games = response.json()
    genres = genres_list(games)
    genre_total_sales = global_sales_per_genre(games, genres)
    return render_template('/games/chart_page2.html', data=genre_total_sales, labels=genres)


def genres_list(games):
    genres = []
    for game in games:
        if game['genre'] not in genres:
            genres.append(game['genre'])
    return genres


def global_sales_per_genre(games, genres):
    genre_total_sales_dict = {i: 0 for i in genres}
    for game in games:
        if game['genre'] in genre_total_sales_dict:
            genre_total_sales_dict[game['genre']] += game['globalSales']
    genre_total_sales = list(genre_total_sales_dict.values())
    return genre_total_sales
