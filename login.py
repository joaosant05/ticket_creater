import tkinter as tk
from tkinter import ttk, messagebox
from extrair_relatorio import ExtrairRelatorio

class Login:
    def __init__(self, root, relatorios, layout, db):
        self.root = root
        self.relatorios = relatorios
        self.layout = layout
        self.db = db
        self.user = tk.StringVar()
        self.tickets_window = None

    def criar_tela_login(self):
        login_frame = ttk.Frame(self.root, padding="10 10 10 10")
        login_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(login_frame, text="Tipo de usuário:", font=("Arial", 11)).grid(column=1, row=1, sticky=tk.W)
        user_combo = ttk.Combobox(login_frame, width=20, textvariable=self.user, values=["Gerar ticket", "Extrair relatorio"])
        user_combo.grid(column=2, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Button(login_frame, text="Login", command=self.login).grid(column=2, row=3, pady=5)

    def login(self):
        user_selection = self.user.get()
        if user_selection == "Gerar ticket":
            self.root.withdraw()
            self.layout.abrir_tela_relatorios()
        elif user_selection == "Extrair relatorio":
            self.root.withdraw()
            extrair_relatorio_window = ExtrairRelatorio(self.root, self.db)
            extrair_relatorio_window.abrir_tela_extrair_relatorio()