import json
from tkinter import *
from tkinter import ttk

class Relatorios:
    def __init__(self):
        self.__usuarios = []
        self.__marcas = []
        self.__organizacoes = []
        self.__navegadores = []
        self.carregar_dados()

    def salvar_dados(self):
        dados = {
            'usuarios': self.__usuarios,
            'marcas': self.__marcas,
            'organizacoes': self.__organizacoes,
            'navegadores': self.__navegadores
        }
        with open('dados.json', 'w') as file:
            json.dump(dados, file)
        print("Dados salvos com sucesso.")

    def carregar_dados(self):
        try:
            with open('dados.json', 'r') as file:
                dados = json.load(file)
                self.__usuarios = dados.get('usuarios', [])
                self.__marcas = dados.get('marcas', [])
                self.__organizacoes = dados.get('organizacoes', [])
                self.__navegadores = dados.get('navegadores', [])
                print("Dados carregados com sucesso.")
        except FileNotFoundError:
            print("Arquivo de dados não encontrado. Usando valores padrão.")

    def abrir_popup_usuario(self, usuario_combo):
        popup = Toplevel()
        popup.title("Adicionar Novo Usuário")

        ttk.Label(popup, text="Novo Usuário:").grid(column=1, row=1, sticky=W)
        novo_usuario_entry = ttk.Entry(popup, width=30)
        novo_usuario_entry.grid(column=2, row=1, padx=5, pady=5, sticky=(W, E))

        def salvar_usuario():
            novo_usuario = novo_usuario_entry.get()
            if novo_usuario and novo_usuario not in self.__usuarios:
                self.__usuarios.append(novo_usuario)
                usuario_combo['values'] = self.__usuarios
                self.salvar_dados()
            popup.destroy()

        ttk.Button(popup, text="Salvar", command=salvar_usuario).grid(column=2, row=2, pady=5)

    def abrir_popup_marca(self, marca_combo):
        popup = Toplevel()
        popup.title("Adicionar Nova Marca")

        ttk.Label(popup, text="Nova Marca:").grid(column=1, row=1, sticky=W)
        nova_marca_entry = ttk.Entry(popup, width=30)
        nova_marca_entry.grid(column=2, row=1, padx=5, pady=5, sticky=(W, E))

        def salvar_marca():
            nova_marca = nova_marca_entry.get()
            if nova_marca not in self.__marcas:
                self.__marcas.append(nova_marca)
                marca_combo['values'] = self.__marcas
                self.salvar_dados()
            popup.destroy()

        ttk.Button(popup, text="Salvar", command=salvar_marca).grid(column=2, row=2, pady=5)

    def abrir_popup_organizacao(self, organizacao_combo):
        popup = Toplevel()
        popup.title("Adicionar Nova Organização")

        ttk.Label(popup, text="Nova Organização:").grid(column=1, row=1, sticky=W)
        nova_organizacao_entry = ttk.Entry(popup, width=30)
        nova_organizacao_entry.grid(column=2, row=1, padx=5, pady=5, sticky=(W, E))

        def salvar_organizacao():
            nova_organizacao = nova_organizacao_entry.get()
            if nova_organizacao not in self.__organizacoes:
                self.__organizacoes.append(nova_organizacao)
                organizacao_combo['values'] = self.__organizacoes
                self.salvar_dados()
            popup.destroy()

        ttk.Button(popup, text="Salvar", command=salvar_organizacao).grid(column=2, row=2, pady=5)

    def abrir_popup_navegador(self, navegador_combo):
        popup = Toplevel()
        popup.title("Adicionar Novo Navegador")

        ttk.Label(popup, text="Novo Navegador:").grid(column=1, row=1, sticky=W)
        nova_navegador_entry = ttk.Entry(popup, width=30)
        nova_navegador_entry.grid(column=2, row=1, padx=5, pady=5, sticky=(W, E))

        def salvar_navegador():
            nova_navegador = nova_navegador_entry.get()
            if nova_navegador not in self.__navegadores:
                self.__navegadores.append(nova_navegador)
                navegador_combo['values'] = self.__navegadores
                self.salvar_dados()
            popup.destroy()

        ttk.Button(popup, text="Salvar", command=salvar_navegador).grid(column=2, row=2, pady=5)
