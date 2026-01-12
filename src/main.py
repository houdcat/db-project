import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from repositories import UserRepository, GameRepository, OrderRepository, ReviewRepository, GenreRepository
from services import ImportService

BG = "#2c2c2c";
SIDEBAR = "#202020";
ACCENT = "#9b59b6";
TXT = "white"
BTN_DEL = "#c0392b";
BTN_EDIT = "#f39c12";
BTN_IMP = "#2980b9";
BTN_ADD = "#27ae60"


class GameStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GameStore")
        self.root.geometry("1400x850")
        self.root.configure(bg=BG)

        self.repos = {
            'user': UserRepository(), 'game': GameRepository(), 'order': OrderRepository(),
            'review': ReviewRepository(), 'genre': GenreRepository()
        }
        self.importer = ImportService()

        self.current_user = self.repos['user'].get_first_user()
        if not self.current_user: self.current_user = {"id": 0, "username": "Guest", "balance": 0}

        self.setup_ui()

    def setup_ui(self):
        self.root.columnconfigure(1, weight=1);
        self.root.rowconfigure(0, weight=1)

        sb = tk.Frame(self.root, bg=SIDEBAR, width=240);
        sb.grid(row=0, column=0, sticky="ns");
        sb.pack_propagate(False)
        tk.Label(sb, text="GAMESTORE", bg=SIDEBAR, fg=ACCENT, font=("Impact", 24)).pack(pady=30)

        # Balance
        self.lbl_bal = tk.Label(sb, text="...", bg=SIDEBAR, fg="white", font=("Arial", 14, "bold"))
        self.lbl_bal.pack(pady=20)
        self.refresh_balance()

        # Menu
        for t, c in [("🎮 Hry", self.view_games), ("🏷 Žánry", self.view_genres), ("👥 Uživatelé", self.view_users),
                     ("⭐ Recenze", self.view_reviews), ("🛒 Objednávky", self.view_orders),
                     ("📊 Reporty", self.view_reports)]:
            tk.Button(sb, text=t, command=c, bg=SIDEBAR, fg=TXT, font=("Segoe UI", 11), relief="flat", anchor="w",
                      padx=20).pack(fill="x", pady=2)

        tk.Button(sb, text="❌ Ukončit", command=self.root.destroy, bg=BTN_DEL, fg=TXT).pack(side="bottom", fill="x",
                                                                                            pady=20)

        self.content = tk.Frame(self.root, bg=BG);
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.view_games()

    def refresh_balance(self):
        try:
            b = self.repos['user'].get_user_balance(self.current_user['id'])
            self.lbl_bal.config(text=f"{b:.2f} Kč")
        except:
            pass

    def clear(self):
        for w in self.content.winfo_children(): w.destroy()

    def run_import(self, import_function, file_type):
        """Otevře dialog a spustí předanou importní funkci"""
        file_path = filedialog.askopenfilename(filetypes=[(file_type.upper(), f"*.{file_type}")])
        if file_path:
            try:
                import_function(file_path)
                messagebox.showinfo("Úspěch",
                                    "Data byla úspěšně importována!\n(Pro zobrazení klikněte znovu na sekci v menu)")
            except Exception as e:
                messagebox.showerror("Chyba importu", f"Nastala chyba:\n{str(e)}")

    def create_toolbar(self, add_fn, edit_fn, del_fn, imp_json_fn, imp_csv_fn, extra_widget=None):
        tf = tk.Frame(self.content, bg=BG);
        tf.pack(fill="x", pady=10)

        def b(t, c, col):
            tk.Button(tf, text=t, command=c, bg=col, fg=TXT, font=("bold", 9)).pack(side="left", padx=5)

        if add_fn: b("➕ Nový", add_fn, BTN_ADD)
        if edit_fn: b("✏ Upravit", edit_fn, BTN_EDIT)
        if del_fn: b("🗑 Smazat", del_fn, BTN_DEL)

        if imp_json_fn:
            b("⬇ JSON", lambda: self.run_import(imp_json_fn, 'json'), BTN_IMP)
        if imp_csv_fn:
            b("⬇ CSV", lambda: self.run_import(imp_csv_fn, 'csv'), BTN_IMP)

        if extra_widget: extra_widget(tf)

    def view_games(self):
        self.clear();
        self.header("Hry")

        def buy_btn(p): tk.Button(p, text="🛒 KOUPIT", bg=ACCENT, fg=TXT, command=self.buy_game).pack(side="left",
                                                                                                     padx=20)

        self.create_toolbar(self.pop_game_add, self.pop_game_edit, self.del_game,
                            self.importer.import_games_json, self.importer.import_games_csv, buy_btn)

        t = self.table(('ID', 'Žánr', 'Název', 'Cena', 'Status', 'Popis'))
        for g in self.repos['game'].get_all_available():
            t.insert('', tk.END, values=(g['id'], g['genre'], g['title'], g['price'], g['status'], g['desc']))
        self.tree = t

    def pop_game_add(self):
        self._game_form("Nová Hra", self.repos['game'].add_game)

    def pop_game_edit(self):
        s = self.tree.selection()
        if s:
            v = self.tree.item(s[0])['values']
            self._game_form("Upravit", lambda g, t, p, d, st: self.repos['game'].update_game(v[0], g, t, p, d, st),
                            {'gid': 1, 't': v[2], 'p': v[3], 'd': v[5], 's': v[4]})

    def _game_form(self, title, cb, data=None):
        win = tk.Toplevel(self.root);
        win.title(title)
        tk.Label(win, text="Genre ID").pack();
        eg = tk.Entry(win);
        eg.pack()
        tk.Label(win, text="Název").pack();
        et = tk.Entry(win);
        et.pack()
        tk.Label(win, text="Cena").pack();
        ep = tk.Entry(win);
        ep.pack()
        tk.Label(win, text="Popis").pack();
        ed = tk.Entry(win);
        ed.pack()
        tk.Label(win, text="Status").pack();
        es = tk.Entry(win);
        es.pack()
        if data:
            eg.insert(0, data.get('gid', 1));
            et.insert(0, data['t']);
            ep.insert(0, data['p']);
            ed.insert(0, data['d']);
            es.insert(0, data['s'])

        def save():
            try:
                cb(int(eg.get()), et.get(), float(ep.get()), ed.get(), es.get()); win.destroy(); self.view_games()
            except Exception as e:
                messagebox.showerror("Err", str(e))

        tk.Button(win, text="OK", command=save).pack()

    def del_game(self):
        s = self.tree.selection()
        if s: self.repos['game'].delete_game(self.tree.item(s[0])['values'][0]); self.view_games()

    def buy_game(self):
        s = self.tree.selection()
        if s:
            try:
                self.repos['order'].create_order_transaction(self.current_user['id'],
                                                             [self.tree.item(s[0])['values'][0]],
                                                             float(self.tree.item(s[0])['values'][3]))
                messagebox.showinfo("OK", "Koupeno");
                self.refresh_balance()
            except Exception as e:
                messagebox.showerror("Err", str(e))

    def view_genres(self):
        self.clear();
        self.header("Žánry")
        # ZDE JE ZMĚNA: Předáváme import funkce místo 0, 0
        self.create_toolbar(self.pop_gen_add, self.pop_gen_edit, self.del_gen,
                            self.importer.import_genres_json, self.importer.import_genres_csv)
        t = self.table(('ID', 'Název'));
        self.tree = t
        for g in self.repos['genre'].get_all_genres(): t.insert('', tk.END, values=(g['id'], g['name']))

    def pop_gen_add(self):
        self._gen_form("Nový", self.repos['genre'].add_genre)

    def pop_gen_edit(self):
        s = self.tree.selection();
        if s: v = self.tree.item(s[0])['values']; self._gen_form("Edit",
                                                                 lambda n: self.repos['genre'].update_genre(v[0], n),
                                                                 v[1])

    def _gen_form(self, t, cb, d=""):
        win = tk.Toplevel(self.root);
        tk.Label(win, text="Jméno").pack();
        e = tk.Entry(win);
        e.pack();
        e.insert(0, d)
        tk.Button(win, text="OK", command=lambda: [cb(e.get()), win.destroy(), self.view_genres()]).pack()

    def del_gen(self):
        s = self.tree.selection();
        if s: self.repos['genre'].delete_genre(self.tree.item(s[0])['values'][0]); self.view_genres()

    def view_users(self):
        self.clear();
        self.header("Uživatelé")
        self.create_toolbar(self.pop_u_add, self.pop_u_edit, self.del_u,
                            self.importer.import_users_json, self.importer.import_users_csv)
        t = self.table(('ID', 'Name', 'Email', 'Bal', 'Adm'));
        self.tree = t
        for u in self.repos['user'].get_all_users(): t.insert('', tk.END,
                                                              values=(u['id'], u['username'], u['email'], u['balance'],
                                                                      u['is_admin']))

    def pop_u_add(self):
        self._u_form("New", self.repos['user'].add_user)

    def pop_u_edit(self):
        s = self.tree.selection()
        if s: v = self.tree.item(s[0])['values']; self._u_form("Edit",
                                                               lambda n, e, a: self.repos['user'].update_user(v[0], e,
                                                                                                              a),
                                                               {'n': v[1], 'e': v[2], 'a': v[4]})

    def _u_form(self, t, cb, d=None):
        win = tk.Toplevel(self.root);
        tk.Label(win, text="Name").pack();
        en = tk.Entry(win);
        en.pack()
        tk.Label(win, text="Email").pack();
        ee = tk.Entry(win);
        ee.pack()
        a = tk.BooleanVar();
        tk.Checkbutton(win, text="Admin", variable=a).pack()
        if d: en.insert(0, d['n']); ee.insert(0, d['e']); a.set(d['a'] == 'True')
        tk.Button(win, text="OK",
                  command=lambda: [cb(en.get(), ee.get(), a.get()), win.destroy(), self.view_users()]).pack()

    def del_u(self):
        s = self.tree.selection();
        if s: self.repos['user'].delete_user(self.tree.item(s[0])['values'][0]); self.view_users()

    def view_reviews(self):
        self.clear();
        self.header("Recenze")
        self.create_toolbar(self.pop_rev_add, self.pop_rev_edit, self.del_rev,
                            self.importer.import_reviews_json, self.importer.import_reviews_csv)
        t = self.table(('ID', 'UID', 'User', 'GID', 'Game', 'Rating', 'Text'))
        for r in self.repos['review'].get_all_reviews():
            t.insert('', tk.END, values=(r['id'], r['uid'], r['user'], r['gid'], r['game'], r['rating'], r['comment']))
        self.tree = t

    def pop_rev_add(self):
        self._rev_form("Nová", self.repos['review'].add_review)

    def pop_rev_edit(self):
        s = self.tree.selection()
        if s:
            v = self.tree.item(s[0])['values']
            self._rev_form("Upravit", lambda u, g, r, c: self.repos['review'].update_review(v[0], u, g, r, c),
                           {'u': v[1], 'g': v[3], 'r': v[5], 'c': v[6]})

    def _rev_form(self, title, cb, data=None):
        win = tk.Toplevel(self.root);
        win.title(title)
        tk.Label(win, text="User ID").pack();
        eu = tk.Entry(win);
        eu.pack()
        tk.Label(win, text="Game ID").pack();
        eg = tk.Entry(win);
        eg.pack()
        tk.Label(win, text="Rating (1-5)").pack();
        er = tk.Entry(win);
        er.pack()
        tk.Label(win, text="Comment").pack();
        ec = tk.Entry(win);
        ec.pack()
        if data: eu.insert(0, data['u']); eg.insert(0, data['g']); er.insert(0, data['r']); ec.insert(0, data['c'])

        def save():
            try:
                cb(int(eu.get()), int(eg.get()), int(er.get()), ec.get()); win.destroy(); self.view_reviews()
            except Exception as e:
                messagebox.showerror("Err", str(e))

        tk.Button(win, text="OK", command=save).pack()

    def del_rev(self):
        s = self.tree.selection()
        if s: self.repos['review'].delete_review(self.tree.item(s[0])['values'][0]); self.view_reviews()

    def view_orders(self):
        self.clear();
        self.header("Objednávky")
        self.create_toolbar(self.pop_ord_add, self.pop_ord_edit, self.del_ord,
                            self.importer.import_orders_json, self.importer.import_orders_csv)
        t = self.table(('ID', 'UID', 'User', 'Total', 'Date'))
        for o in self.repos['order'].get_all_orders():
            t.insert('', tk.END, values=(o['id'], o['uid'], o['username'], o['total'], o['date']))
        self.tree = t

    def pop_ord_add(self):
        self._ord_form("Nová", self.repos['order'].add_order)

    def pop_ord_edit(self):
        s = self.tree.selection()
        if s:
            v = self.tree.item(s[0])['values']
            self._ord_form("Upravit", lambda u, t: self.repos['order'].update_order(v[0], u, t), {'u': v[1], 't': v[3]})

    def _ord_form(self, title, cb, data=None):
        win = tk.Toplevel(self.root);
        win.title(title)
        tk.Label(win, text="User ID").pack();
        eu = tk.Entry(win);
        eu.pack()
        tk.Label(win, text="Total").pack();
        et = tk.Entry(win);
        et.pack()
        if data: eu.insert(0, data['u']); et.insert(0, data['t'])

        def save():
            try:
                cb(int(eu.get()), float(et.get())); win.destroy(); self.view_orders()
            except Exception as e:
                messagebox.showerror("Err", str(e))

        tk.Button(win, text="OK", command=save).pack()

    def del_ord(self):
        s = self.tree.selection()
        if s: self.repos['order'].delete_order(self.tree.item(s[0])['values'][0]); self.view_orders()

    def view_reports(self):
        self.clear();
        self.header("Report")
        t = tk.Text(self.content, bg="#34495e", fg="white");
        t.pack(fill="both")
        try:
            for r in self.repos['order'].get_report_data(): t.insert(tk.END, str(r) + "\n")
        except:
            t.insert(tk.END, "Žádná data")

    def header(self, t):
        tk.Label(self.content, text=t, font=("Arial", 24), bg=BG, fg=TXT).pack(pady=10)

    def table(self, c):
        f = tk.Frame(self.content);
        f.pack(fill="both", expand=True);
        sb = ttk.Scrollbar(f);
        sb.pack(side="right", fill="y")
        t = ttk.Treeview(f, columns=c, show='headings', yscrollcommand=sb.set);
        t.pack(fill="both", expand=True);
        sb.config(command=t.yview)
        for i in c: t.heading(i, text=i); t.column(i, width=80)
        return t


if __name__ == "__main__":
    root = tk.Tk();
    app = GameStoreApp(root);
    root.mainloop()