import json
import csv
from repositories import UserRepository, GameRepository, OrderRepository, ReviewRepository, GenreRepository

class ImportService:
    def __init__(self):
        self.repos = {
            'user': UserRepository(),
            'game': GameRepository(),
            'order': OrderRepository(),
            'review': ReviewRepository(),
            'genre': GenreRepository()
        }

    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_csv(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Přeskočit hlavičku
            return list(reader)

    # HRY
    def import_games_json(self, path):
        data = self._load_json(path)
        for i in data:
            # Očekává: genre_id, title, price, desc, status
            self.repos['game'].add_game(i.get('genre_id', 1), i['title'], float(i['price']), i.get('desc', ''), i.get('status', 'Available'))

    def import_games_csv(self, path):
        data = self._load_csv(path)
        for r in data:
            # CSV: GenreID, Title, Price, Desc, Status
            self.repos['game'].add_game(int(r[0]), r[1], float(r[2]), r[3], r[4])

    # UŽIVATELÉ
    def import_users_json(self, path):
        data = self._load_json(path)
        for i in data:
            self.repos['user'].add_user(i['username'], i['email'], i.get('is_admin', False))

    def import_users_csv(self, path):
        data = self._load_csv(path)
        for r in data:
            # CSV: Username, Email, IsAdmin
            self.repos['user'].add_user(r[0], r[1], r[2] == 'True')

    # ŽÁNRY
    def import_genres_json(self, path):
        data = self._load_json(path)
        for i in data:
            self.repos['genre'].add_genre(i['name'])

    def import_genres_csv(self, path):
        data = self._load_csv(path)
        for r in data:
            # CSV: Name
            self.repos['genre'].add_genre(r[0])

    # RECENZE
    def import_reviews_json(self, path):
        data = self._load_json(path)
        for i in data:
            self.repos['review'].add_review(i['user_id'], i['game_id'], int(i['rating']), i['comment'])

    def import_reviews_csv(self, path):
        data = self._load_csv(path)
        for r in data:
            # CSV: UserID, GameID, Rating, Comment
            self.repos['review'].add_review(int(r[0]), int(r[1]), int(r[2]), r[3])

    # OBJEDNÁVKY
    def import_orders_json(self, path):
        data = self._load_json(path)
        for i in data:
            self.repos['order'].add_order(i['user_id'], float(i['total']))

    def import_orders_csv(self, path):
        data = self._load_csv(path)
        for r in data:
            # CSV: UserID, Total
            self.repos['order'].add_order(int(r[0]), float(r[1]))