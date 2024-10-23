from tkinter import Tk
from database import Database
from relatorios import Relatorios
from layout import Layout
from login import Login
from extrair_relatorio import ExtrairRelatorio

if __name__ == "__main__":
    
    root = Tk()
    root.title("Sistema de Relatórios")

    db = Database()
    relatorios = Relatorios()

    login = Login(root, relatorios, None, db)
    
    extrair_relatorio = ExtrairRelatorio(root, db, login)

    layout = Layout(root, relatorios, db, extrair_relatorio)
    
    login.layout = layout

    login.criar_tela_login()
    root.mainloop()
