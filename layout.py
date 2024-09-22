from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tickets import Tickets

class Layout:
    def __init__(self, root, relatorios, db, login_screen):
        self.root = root
        self.relatorios = relatorios
        self.db = db
        self.login_screen = login_screen
        self.relatorios_root = None 
        self.tier_var = StringVar()
        self.ambiente_var = StringVar()
        self.frequencia_var = StringVar()
        self.usuario_var = StringVar()
        self.navegador_var = StringVar()
        self.organizacao_var = StringVar()
        self.marca_var = StringVar()
        self.anexos = []

    def abrir_tela_relatorios(self):
        if self.relatorios_root is not None:
            self.relatorios_root.destroy()

        self.relatorios_root = Toplevel(self.root)
        self.relatorios_root.title("Acompanhamento Revisões")
        self.relatorios_root.geometry("750x690")

        mainframe = ttk.Frame(self.relatorios_root, padding="15 15 15 15")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.relatorios_root.columnconfigure(0, weight=1)
        self.relatorios_root.rowconfigure(0, weight=1)

        # Widgets
        ttk.Label(mainframe, text="Tier:", font=("Arial", 11)).grid(column=1, row=1, sticky=W, padx=4, pady=4)
        tier_combo = ttk.Combobox(mainframe, width=20, textvariable=self.tier_var, values=["Tier 1", "Tier 2", "Tier 3"])
        tier_combo.grid(column=2, row=1, sticky=(W, E), padx=4, pady=4)

        ttk.Label(mainframe, text="Ambiente:", font=("Arial", 11)).grid(column=1, row=2, sticky=W, padx=4, pady=4)
        ambiente_combo = ttk.Combobox(mainframe, width=20, textvariable=self.ambiente_var, values=["Desenvolvimento", "Homologação", "Produção"])
        ambiente_combo.grid(column=2, row=2, sticky=(W, E), padx=4, pady=4)

        ttk.Label(mainframe, text="Frequência:", font=("Arial", 11)).grid(column=1, row=3, sticky=W, padx=4, pady=4)
        frequencia_combo = ttk.Combobox(mainframe, width=20, textvariable=self.frequencia_var, values=["1", "2", "3"])
        frequencia_combo.grid(column=2, row=3, sticky=(W, E), padx=4, pady=4)

        ttk.Label(mainframe, text="Usuário:", font=("Arial", 11)).grid(column=1, row=4, sticky=W, padx=4, pady=4)
        usuario_combo = ttk.Combobox(mainframe, width=20, textvariable=self.usuario_var, values=self.relatorios._Relatorios__usuarios)
        usuario_combo.grid(column=2, row=4, sticky=(W, E), padx=4, pady=4)
        ttk.Button(mainframe, text="+", command=lambda: self.relatorios.abrir_popup_usuario(usuario_combo)).grid(column=3, row=4, padx=4, pady=4)

        ttk.Label(mainframe, text="Navegador:", font=("Arial", 11)).grid(column=1, row=5, sticky=W, padx=4, pady=4)
        navegador_combo = ttk.Combobox(mainframe, width=20, textvariable=self.navegador_var, values=self.relatorios._Relatorios__navegadores)
        navegador_combo.grid(column=2, row=5, sticky=(W, E), padx=4, pady=4)
        ttk.Button(mainframe, text="+", command=lambda: self.relatorios.abrir_popup_navegador(navegador_combo)).grid(column=3, row=5, padx=4, pady=4)

        ttk.Label(mainframe, text="Organização:", font=("Arial", 11)).grid(column=1, row=6, sticky=W, padx=4, pady=4)
        organizacao_combo = ttk.Combobox(mainframe, width=20, textvariable=self.organizacao_var, values=self.relatorios._Relatorios__organizacoes)
        organizacao_combo.grid(column=2, row=6, sticky=(W, E), padx=4, pady=4)
        ttk.Button(mainframe, text="+", command=lambda: self.relatorios.abrir_popup_organizacao(organizacao_combo)).grid(column=3, row=6, padx=4, pady=4)

        ttk.Label(mainframe, text="Marca:", font=("Arial", 11)).grid(column=1, row=7, sticky=W, padx=4, pady=4)
        marca_combo = ttk.Combobox(mainframe, width=20, textvariable=self.marca_var, values=self.relatorios._Relatorios__marcas)
        marca_combo.grid(column=2, row=7, sticky=(W, E), padx=4, pady=4)
        ttk.Button(mainframe, text="+", command=lambda: self.relatorios.abrir_popup_marca(marca_combo)).grid(column=3, row=7, padx=4, pady=4)

        ttk.Label(mainframe, text="Log:", font=("Arial", 11)).grid(column=1, row=8, sticky=W, padx=4, pady=4)
        self.log_text = Text(mainframe, width=50, height=4, wrap=WORD)
        self.log_text.grid(column=2, row=8, columnspan=2, sticky=(W, E), padx=4, pady=4)

        ttk.Label(mainframe, text="Como Reproduzir:", font=("Arial", 11)).grid(column=1, row=9, sticky=W, padx=4, pady=4)
        self.como_reproduzir_text = Text(mainframe, width=50, height=4, wrap=WORD)
        self.como_reproduzir_text.grid(column=2, row=9, columnspan=2, sticky=(W, E), padx=4, pady=4)

        ttk.Label(mainframe, text="O Que Acontece:", font=("Arial", 11)).grid(column=1, row=10, sticky=W, padx=4, pady=4)
        self.o_que_acontece_text = Text(mainframe, width=50, height=4, wrap=WORD)
        self.o_que_acontece_text.grid(column=2, row=10, columnspan=2, sticky=(W, E), padx=4, pady=4)

        ttk.Label(mainframe, text="O Que Deveria Acontecer:", font=("Arial", 11)).grid(column=1, row=11, sticky=W, padx=4, pady=4)
        self.o_que_deveria_acontecer_text = Text(mainframe, width=50, height=4, wrap=WORD)
        self.o_que_deveria_acontecer_text.grid(column=2, row=11, columnspan=2, sticky=(W, E), padx=4, pady=4)

        ttk.Button(mainframe, text="Selecionar Arquivo", command=self.selecionar_arquivo).grid(column=2, row=12, columnspan=2, pady=10)
        ttk.Button(mainframe, text="Enviar", command=self.enviar_dados).grid(column=2, row=13, columnspan=2, pady=10)
        ttk.Button(mainframe, text="Voltar", command=self.voltar_para_login).grid(column=0, row=14, columnspan=2, pady=10)

        # Tela de tickets existentes
        ttk.Button(mainframe, text="Tickets", command=self.abrir_tickets).grid(column=4, row=14, columnspan=2, pady=10)

    def abrir_tickets(self):
        if self.relatorios_root is not None:
            tickets = Tickets(self.root, self.db)
            tickets.abrir_tela_tickets()

    def voltar_para_login(self):
        if self.relatorios_root is not None:
            self.relatorios_root.destroy()
            self.relatorios_root = None
        self.root.deiconify()

    def selecionar_arquivo(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*"), ("Image Files", "*.jpg;*.jpeg;*.png"), ("Video Files", "*.mp4;*.avi")])
        if file_paths:
            self.anexos = []
            for file_path in file_paths:
                with open(file_path, 'rb') as file:
                    self.anexos.append(file.read())
            print(f"{len(self.anexos)} arquivos selecionados.")

    def enviar_dados(self):
        # Salva os dados principais
        dados = (
            self.tier_var.get(),
            self.ambiente_var.get(),
            self.frequencia_var.get(),
            self.usuario_var.get(),
            self.navegador_var.get(),
            self.organizacao_var.get(),
            self.marca_var.get(),
            self.log_text.get("1.0", "end-1c"),
            self.como_reproduzir_text.get("1.0", "end-1c"),
            self.o_que_acontece_text.get("1.0", "end-1c"),
            self.o_que_deveria_acontecer_text.get("1.0", "end-1c"),
        )
        
        # Salva os dados na tabela
        ticket_id = self.db.salvar_dados(dados)
        
        # Salva anexos se houver
        if self.anexos:
            for anexo_blob in self.anexos:
                self.db.salvar_anexo(ticket_id, anexo_blob)

        # Limpa os campos de entrada
        self.limpar_campos()

    def limpar_campos(self):
        self.log_text.delete("1.0", "end")
        self.como_reproduzir_text.delete("1.0", "end")
        self.o_que_acontece_text.delete("1.0", "end")
        self.o_que_deveria_acontecer_text.delete("1.0", "end")
        self.anexos = []
