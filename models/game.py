


class Game:
    def __init__(self):
        self.id = games_data['_id']
        self.rank = games_data['rank']
        self.name = games_data['name']
        self.platform = games_data['platform']
        self.year = games_data['year']
        self.genre = games_data['genre']
        self.publisher = games_data['publisher']
        self.naSales = games_data['naSales']
        self.euSales = games_data['euSales']
        self.jpSales = games_data['jpSales']
        self.otherSales = games_data['otherSales']
        self.globalSales = games_data['globalSales']


        @staticmethod
        def game_decoder(obj):
            return Game(obj)