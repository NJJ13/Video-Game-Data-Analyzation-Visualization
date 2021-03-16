from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import requests
import json
from types import SimpleNamespace

bp = Blueprint('games', __name__)


@bp.route('/games')
def display_games():
    response = requests.get('https://api.dccresource.com/api/games')
    games_data = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    return render_template('games/index.html', games_data)
