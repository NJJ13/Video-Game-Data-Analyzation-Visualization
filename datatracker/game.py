from flask import Blueprint, render_template
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
