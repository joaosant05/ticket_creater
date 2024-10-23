import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error

class Tickets:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.tickets_window = None

    def abrir_tela_tickets(self):
        if self.tickets_window is not None:
            self.tickets_window.destroy()

        self.tickets_window = tk.Toplevel(self.root)
        self.tickets_window.title("Tickets Cadastrados")
        self.tickets_window.geometry("1750x300")
        self.tickets_window.resizable(True, True)

        # Frame principal
        mainframe = ttk.Frame(self.tickets_window)
        mainframe.pack(fill=tk.BOTH, expand=True)

        # Criação da barra de rolagem
        self.v_scrollbar = ttk.Scrollbar(mainframe, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar = ttk.Scrollbar(mainframe, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        self.tree = ttk.Treeview(mainframe, columns=("ID", "Tier", "Ambiente", "Frequência", "Usuário", "Navegador", "Organização", "Marca", "Log", "Como Reproduzir", "O Que Acontece", "O Que Deveria Acontecer", "Criado Em", "Ações"), show='headings',
                                 yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        col_widths = {
            "ID": 20,
            "Tier": 40,
            "Ambiente": 80,
            "Frequência": 80,
            "Usuário": 150,
            "Navegador": 80,
            "Organização": 80,
            "Marca": 80,
            "Log": 200,
            "Como Reproduzir": 200,
            "O Que Acontece": 200,
            "O Que Deveria Acontecer": 200,
            "Criado Em": 150,
            "Ações": 60 
        }

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col], anchor=tk.W, stretch=tk.NO)

        # Configuração das barras de rolagem
        self.v_scrollbar.config(command=self.tree.yview)
        self.h_scrollbar.config(command=self.tree.xview)

        # Botões
        ttk.Button(mainframe, text="Atualizar", command=self.atualizar_tickets).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(mainframe, text="Editar Ticket", command=self.editar_ticket_selecionado).pack(side=tk.LEFT, padx=5, pady=5)

        self.atualizar_tickets()

    def atualizar_tickets(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        connection = self.db.conectar_banco()
        if connection is not None:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM relatorios"
                cursor.execute(query)
                tickets = cursor.fetchall()

                for ticket in tickets:
                    self.tree.insert("", tk.END, values=(
                        ticket.get("id"),
                        ticket.get("tier"),
                        ticket.get("ambiente"),
                        ticket.get("frequencia"),
                        ticket.get("usuario"),
                        ticket.get("navegador"),
                        ticket.get("organizacao"),
                        ticket.get("marca"),
                        ticket.get("log"),
                        ticket.get("como_reproduzir"),
                        ticket.get("o_que_acontece"),
                        ticket.get("o_que_deveria_acontecer"),
                        ticket.get("created_at"),
                        "Excluir"
                    ))
                    # Bind na coluna de Ações para deletar
                    self.tree.bind("<Double-1>", self.on_treeview_double_click)
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao buscar tickets do MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def on_treeview_double_click(self, event):
        item = self.tree.selection()
        if item:
            item_values = self.tree.item(item, "values")
            ticket_id = item_values[0]
            self.deletar_ticket(ticket_id)

    def deletar_ticket(self, ticket_id):
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o ticket ID: {ticket_id}?"):
            connection = self.db.conectar_banco()
            if connection is not None:
                try:
                    cursor = connection.cursor()
                    
                    # Deletar anexos associados ao ticket
                    delete_anexos_query = "DELETE FROM anexos WHERE ticket_id = %s"
                    cursor.execute(delete_anexos_query, (ticket_id,))
                    
                    delete_ticket_query = "DELETE FROM relatorios WHERE id = %s"
                    cursor.execute(delete_ticket_query, (ticket_id,))
                    
                    connection.commit()
                    messagebox.showinfo("Sucesso", "Ticket e anexos excluídos com sucesso.")
                    self.atualizar_tickets()
                except Error as e:
                    messagebox.showerror("Erro", f"Erro ao excluir o ticket: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()

    def editar_ticket_selecionado(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um ticket para editar.")
            return

        selected_ticket = self.tree.item(selected_item)["values"]
        self.selected_ticket_id = selected_ticket[0]

        # Janela de edição
        self.edit_window = tk.Toplevel(self.tickets_window)
        self.edit_window.title(f"Editar Ticket ID: {self.selected_ticket_id}")
        self.edit_window.geometry("520x785")

        edit_frame = ttk.Frame(self.edit_window)
        edit_frame.pack(fill=tk.BOTH, expand=True)

        # Criação do Canvas
        canvas = tk.Canvas(edit_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scrollbar_edit = ttk.Scrollbar(edit_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.v_scrollbar_edit.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=self.v_scrollbar_edit.set)

        input_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=input_frame, anchor="nw")

        fields = {
            "Tier": selected_ticket[1],
            "Ambiente": selected_ticket[2],
            "Frequência": selected_ticket[3],
            "Usuário": selected_ticket[4],
            "Navegador": selected_ticket[5],
            "Organização": selected_ticket[6],
            "Marca": selected_ticket[7],
            "Log": selected_ticket[8],
            "Como Reproduzir": selected_ticket[9],
            "O Que Acontece": selected_ticket[10],
            "O Que Deveria Acontecer": selected_ticket[11],
        }

        self.edit_entries = {}
        row = 0

        small_height = 1
        large_height = 7

        for label, value in fields.items():
            ttk.Label(input_frame, text=label).grid(column=0, row=row, padx=10, pady=5, sticky=tk.W)
            
            height = small_height if label in ["Tier", "Ambiente", "Frequência", "Usuário", "Navegador", "Organização", "Marca"] else large_height
            text_widget = tk.Text(input_frame, width=40, height=height, wrap=tk.WORD)
            text_widget.insert(tk.END, value)
            text_widget.grid(column=1, row=row, padx=10, pady=5)
            self.edit_entries[label] = text_widget
            row += 1

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        input_frame.bind("<Configure>", on_frame_configure)

        save_button = ttk.Button(self.edit_window, text="Salvar Alterações", command=self.salvar_edicao)
        save_button.pack(pady=20)

        input_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        save_button.pack(side=tk.BOTTOM, pady=10)
        
    def salvar_edicao(self):
        updated_data = {label: widget.get("1.0", "end-1c") for label, widget in self.edit_entries.items()}

        connection = self.db.conectar_banco()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = """
                UPDATE relatorios
                SET tier = %s, ambiente = %s, frequencia = %s, usuario = %s, navegador = %s,
                    organizacao = %s, marca = %s, log = %s, como_reproduzir = %s,
                    o_que_acontece = %s, o_que_deveria_acontecer = %s
                WHERE id = %s
                """
                data = (
                    updated_data["Tier"],
                    updated_data["Ambiente"],
                    updated_data["Frequência"],
                    updated_data["Usuário"],
                    updated_data["Navegador"],
                    updated_data["Organização"],
                    updated_data["Marca"],
                    updated_data["Log"],
                    updated_data["Como Reproduzir"],
                    updated_data["O Que Acontece"],
                    updated_data["O Que Deveria Acontecer"],
                    self.selected_ticket_id
                )
                cursor.execute(query, data)
                connection.commit()

                messagebox.showinfo("Sucesso", "Ticket atualizado com sucesso.")
                self.edit_window.destroy()
                self.atualizar_tickets()
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao atualizar o ticket: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
