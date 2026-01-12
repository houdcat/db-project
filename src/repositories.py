from database import Database


class BaseRepository:
    def __init__(self):
        self.db = Database()


class UserRepository(BaseRepository):
    def get_all_users(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT UserID, Username, Email, WalletBalance, IsAdmin FROM Users")
        return [{"id": r.UserID, "username": r.Username, "email": r.Email, "balance": r.WalletBalance,
                 "is_admin": r.IsAdmin} for r in cursor.fetchall()]

    def get_first_user(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT TOP 1 UserID, Username, WalletBalance, IsAdmin FROM Users")
        row = cursor.fetchone()
        return {"id": row.UserID, "username": row.Username, "balance": row.WalletBalance,
                "is_admin": row.IsAdmin} if row else None

    def get_user_balance(self, uid):
        c = self.db.get_cursor();
        c.execute("SELECT WalletBalance FROM Users WHERE UserID=?", (uid,));
        r = c.fetchone()
        return r[0] if r else 0.0

    def add_user(self, u, e, a):
        self.db.get_cursor().execute("INSERT INTO Users (Username, Email, IsAdmin) VALUES (?, ?, ?)", (u, e, a));
        self.db.connection.commit()

    def update_user(self, uid, e, a):
        self.db.get_cursor().execute("UPDATE Users SET Email=?, IsAdmin=? WHERE UserID=?", (e, a, uid));
        self.db.connection.commit()

    def delete_user(self, uid):
        self.db.get_cursor().execute("DELETE FROM Users WHERE UserID=?", (uid,));
        self.db.connection.commit()


class GameRepository(BaseRepository):
    def get_all_available(self):
        cursor = self.db.get_cursor()
        # JOIN s Genres pro získání jména žánru
        sql = """SELECT g.GameID, g.GenreID, gen.Name, g.Title, g.Price, g.Status, g.Description 
                 FROM Games g LEFT JOIN Genres gen ON g.GenreID = gen.GenreID"""
        cursor.execute(sql)
        return [
            {"id": r.GameID, "gid": r.GenreID, "genre": r.Name, "title": r.Title, "price": r.Price, "status": r.Status,
             "desc": r.Description} for r in cursor.fetchall()]

    def add_game(self, gid, title, price, desc, status):
        if price < 0: raise ValueError("Cena nesmí být záporná")
        self.db.get_cursor().execute(
            "INSERT INTO Games (GenreID, Title, Price, Description, Status) VALUES (?, ?, ?, ?, ?)",
            (gid, title, price, desc, status))
        self.db.connection.commit()

    def update_game(self, game_id, gid, title, price, desc, status):
        if price < 0: raise ValueError("Cena nesmí být záporná")
        self.db.get_cursor().execute(
            "UPDATE Games SET GenreID=?, Title=?, Price=?, Description=?, Status=? WHERE GameID=?",
            (gid, title, price, desc, status, game_id))
        self.db.connection.commit()

    def delete_game(self, game_id):
        self.db.get_cursor().execute("DELETE FROM Games WHERE GameID=?", (game_id,));
        self.db.connection.commit()


class GenreRepository(BaseRepository):
    def get_all_genres(self):
        c = self.db.get_cursor();
        c.execute("SELECT GenreID, Name FROM Genres");
        return [{"id": r.GenreID, "name": r.Name} for r in c.fetchall()]

    def add_genre(self, n):
        self.db.get_cursor().execute("INSERT INTO Genres (Name) VALUES (?)", (n,));
        self.db.connection.commit()

    def update_genre(self, gid, n):
        self.db.get_cursor().execute("UPDATE Genres SET Name=? WHERE GenreID=?", (n, gid));
        self.db.connection.commit()

    def delete_genre(self, gid):
        self.db.get_cursor().execute("DELETE FROM Genres WHERE GenreID=?", (gid,));
        self.db.connection.commit()


class ReviewRepository(BaseRepository):
    def get_all_reviews(self):
        cursor = self.db.get_cursor()
        # Získáváme UserID i Username, GameID i Title
        sql = """SELECT r.ReviewID, r.UserID, u.Username, r.GameID, g.Title, r.Rating, r.Comment, r.ReviewDate 
                 FROM Reviews r 
                 JOIN Users u ON r.UserID = u.UserID 
                 JOIN Games g ON r.GameID = g.GameID"""
        cursor.execute(sql)
        return [{"id": r.ReviewID, "uid": r.UserID, "user": r.Username, "gid": r.GameID, "game": r.Title,
                 "rating": r.Rating, "comment": r.Comment, "date": r.ReviewDate} for r in cursor.fetchall()]

    def add_review(self, uid, gid, rating, comment):
        if not (1 <= rating <= 5): raise ValueError("Rating 1-5")
        self.db.get_cursor().execute("INSERT INTO Reviews (UserID, GameID, Rating, Comment) VALUES (?, ?, ?, ?)",
                                     (uid, gid, rating, comment))
        self.db.connection.commit()

    def update_review(self, rid, uid, gid, rating, comment):
        if not (1 <= rating <= 5): raise ValueError("Rating 1-5")
        self.db.get_cursor().execute("UPDATE Reviews SET UserID=?, GameID=?, Rating=?, Comment=? WHERE ReviewID=?",
                                     (uid, gid, rating, comment, rid))
        self.db.connection.commit()

    def delete_review(self, rid):
        self.db.get_cursor().execute("DELETE FROM Reviews WHERE ReviewID=?", (rid,));
        self.db.connection.commit()


class OrderRepository(BaseRepository):
    def get_all_orders(self):
        cursor = self.db.get_cursor()
        sql = """SELECT o.OrderID, o.UserID, u.Username, o.TotalAmount, o.OrderDate FROM Orders o 
                 JOIN Users u ON o.UserID = u.UserID ORDER BY o.OrderDate DESC"""
        cursor.execute(sql)
        return [{"id": r.OrderID, "uid": r.UserID, "username": r.Username, "total": r.TotalAmount, "date": r.OrderDate}
                for r in cursor.fetchall()]

    def add_order(self, uid, total):
        self.db.get_cursor().execute("INSERT INTO Orders (UserID, TotalAmount) VALUES (?, ?)", (uid, total));
        self.db.connection.commit()

    def update_order(self, oid, uid, total):
        self.db.get_cursor().execute("UPDATE Orders SET UserID=?, TotalAmount=? WHERE OrderID=?", (uid, total, oid));
        self.db.connection.commit()

    def delete_order(self, oid):
        self.db.get_cursor().execute("DELETE FROM Orders WHERE OrderID=?", (oid,));
        self.db.connection.commit()

    def create_order_transaction(self, user_id, game_ids, total_price):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT WalletBalance FROM Users WHERE UserID = ?", (user_id,))
            res = cursor.fetchone()
            if not res: raise ValueError("User nenalezen")
            if res[0] < total_price: raise ValueError("Nedostatek kreditu")

            cursor.execute("INSERT INTO Orders (UserID, TotalAmount) OUTPUT INSERTED.OrderID VALUES (?, ?)",
                           (user_id, total_price))
            oid = cursor.fetchone()[0]
            for gid in game_ids:
                cursor.execute("INSERT INTO OrderItems (OrderID, GameID, PriceAtPurchase) VALUES (?, ?, ?)",
                               (oid, gid, total_price))  # zjednoduseno
            cursor.execute("UPDATE Users SET WalletBalance = WalletBalance - ? WHERE UserID = ?",
                           (total_price, user_id))
            self.db.connection.commit()
        except Exception as e:
            self.db.connection.rollback();
            raise e

    def get_report_data(self):
        c = self.db.get_cursor();
        c.execute("SELECT * FROM v_UserActivity");
        return c.fetchall()