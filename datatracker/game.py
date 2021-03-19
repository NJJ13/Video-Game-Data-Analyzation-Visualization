from flask import Blueprint, render_template, request, flash, redirect, url_for

import requests, json, operator, math
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
            global_sales_dict[game.platform] = round(global_sales_dict[game.platform], 2) + round(game.globalSales, 2)

    global_sales = list(global_sales_dict.values())

    return render_template('games/platform.html', global_sales_dict=global_sales_dict, labels=consoles,
                           values=global_sales)


@bp.route('/gameID/<id>', methods=['GET'])
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
    labels = []
    values = []
    for game in games:
        if game.name == name:
            cross_platform_game.append(game)
            labels.append(game.platform)
            values.append(game.globalSales)
    return render_template('games/console_breakdown.html', cross_platform_game=cross_platform_game, labels=labels,
                           values=values)


@bp.route('/genre')
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
            genre_total_sales_dict[game['genre']] = round(genre_total_sales_dict[game['genre']] ,2) + round(game['globalSales'],2)
    genre_total_sales = list(genre_total_sales_dict.values())
    return genre_total_sales

@bp.route('/publisher', methods=['GET'])
def successful_publishers():
    response = requests.get('https://api.dccresource.com/api/games')
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    publishers = get_publishers(games)
    consoles = get_consoles(games)
    console_publisher_success_dict = {}
    for console in consoles:
        publisher_dict = {i: 0 for i in publishers}
        for game in games:
            if game.platform == console:
                  publisher_dict[game.publisher] += game.globalSales

        most_sales = max(publisher_dict.values())
        publisher = get_key(publisher_dict, most_sales)
        console_publisher_success_dict[console + "-" + publisher] = round(most_sales, 2)
    console_and_publisher = list(console_publisher_success_dict.keys())
    console_and_publisher_sales = list(console_publisher_success_dict.values())

    return render_template('games/best_publishers_by_console.html', labels=console_and_publisher,
                           values=console_and_publisher_sales)


def get_publishers(games):
    publishers = []
    for game in games:
        if game.publisher not in publishers:
            publishers.append(game.publisher)

    return publishers


def get_consoles(games):
    consoles = []
    for game in games:
        if game.platform not in consoles:
            consoles.append(game.platform)

    return consoles

def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key

