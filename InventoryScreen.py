# InventoryScreen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from DB.database_stockroom import get_stockroom_items, add_stockroom_item, remove_stockroom_item
from DB.database_item_codes import get_item_codes

class InventoryScreen(ttk.Frame):
    def __init__(self, parent, user):
        """
        user: tupla com os dados do usuário, ex:
              [id, name, email, password, continent, location, department]
        """
        super().__init__(parent)
        self.user = user
        self.pack(fill="both", expand=True)
        
        self.filter_vars = {}
        self.create_widgets()
        # Em vez de load_items(), use search_items() para aplicar os filtros já na inicialização
        self.search_items()

    def create_widgets(self):
        # Define estilo customizado para botões com tamanho menor
        style = ttk.Style()
        style.configure("Small.TButton", padding=(4, 2), font=("TkDefaultFont", 8))
        
        # Frame superior para botões e filtros
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        # Botão "Cadastrar Item" - à esquerda, com estilo menor
        self.btn_add = ttk.Button(top_frame, text="Cadastrar Item", command=self.open_add_item_popup, style="Small.TButton", width=12)
        self.btn_add.pack(side="left", padx=(0, 5))
        
        # Botão "Remover Item" - ao lado de "Cadastrar Item"
        self.btn_remove = ttk.Button(top_frame, text="Remover Item", command=self.remove_selected_item, style="Small.TButton", width=12)
        self.btn_remove.pack(side="left", padx=(0, 20))

        # Frame de filtros
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side="left", fill="x", expand=True)
        
        # Filtros convencionais: Código, Nome, Usuário, Cadastro
        filtros = [
            ("Código", "item_code"),
            ("Nome", "item_name"),
            ("Usuário", "user_name"),
            ("Cadastro", "created_date")
        ]
        
        for label_text, key in filtros:
            lbl = ttk.Label(search_frame, text=label_text)
            lbl.pack(side="left", padx=(5,2))
            lbl.configure(font=("TkDefaultFont", 8))
            var = tk.StringVar()
            entry = ttk.Entry(search_frame, textvariable=var, width=10)
            entry.pack(side="left", padx=(0,5))
            self.filter_vars[key] = var
        
        # Filtro "Removido" (checkbox)
        # Se marcado, filtra itens com removed_date != NULL (itens removidos)
        # Se desmarcado, filtra itens com removed_date == NULL (itens ativos)
        self.removed_var = tk.BooleanVar(value=False)
        self.filter_vars['removed'] = self.removed_var
        
        chk_removed = ttk.Checkbutton(
            search_frame,
            text="Removido",
            variable=self.removed_var,
            command=self.search_items
        )
        chk_removed.pack(side="left", padx=5)
        
        # Botão de buscar com estilo menor
        self.btn_search = ttk.Button(search_frame, text="Buscar", command=self.search_items, style="Small.TButton", width=8)
        self.btn_search.pack(side="left", padx=5)
        
        # Treeview para listagem dos itens
        columns = ("id", "item_code", "item_name", "user_name", "created_date", "removed_date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Definições de cabeçalho
        self.tree.heading("item_code", text="Código")
        self.tree.heading("item_name", text="Nome")
        self.tree.heading("user_name", text="Usuário")
        self.tree.heading("created_date", text="Cadastro")
        self.tree.heading("removed_date", text="Removido")
        
        # Opcionalmente, ocultar a coluna "id"
        self.tree.column("id", width=0, stretch=False)
    
    def load_items(self, filters=None):
        # Limpa o Treeview
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)
        
        # Local e dept do usuário logado
        location = self.user[5]
        department = self.user[6]
        
        # Consulta os itens do estoque
        items = get_stockroom_items(location, department, filters)
        
        for row in items:
            # row: (id, item_code, item_name, user_name, created_date, removed_date)
            criado = row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else ""
            removido = row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else ""
            
            self.tree.insert(
                "",
                "end",
                values=(row[0], row[1], row[2], row[3], criado, removido)
            )
    
    def search_items(self):
        # Monta o dicionário de filtros
        filters = {}
        filters['item_code'] = self.filter_vars['item_code'].get().strip()
        filters['item_name'] = self.filter_vars['item_name'].get().strip()
        filters['user_name'] = self.filter_vars['user_name'].get().strip()
        filters['created_date'] = self.filter_vars['created_date'].get().strip()
        filters['removed'] = self.removed_var.get()

        self.load_items(filters)
    
    def remove_selected_item(self):
        """
        Remove o item selecionado, marcando sua removed_date = NOW().
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um item para remover.")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja remover o(s) item(ns) selecionado(s)?"):
            for sel in selected:
                values = self.tree.item(sel, "values")
                item_id = values[0]
                remove_stockroom_item(item_id)
            self.search_items()

    def open_add_item_popup(self):
        # Pop up para cadastro de novo item
        popup = tk.Toplevel(self)
        popup.title("Cadastrar Item")
        popup.geometry("300x200")
        
        lbl_code = ttk.Label(popup, text="Código do Item:")
        lbl_code.pack(pady=5)
        
        codes = get_item_codes()  # Lista de (code, name)
        code_options = [f"{code} - {name}" for code, name in codes]
        
        code_var = tk.StringVar()
        cmb_code = ttk.Combobox(popup, textvariable=code_var, values=code_options, state="readonly", width=20)
        cmb_code.pack(pady=5)
        
        lbl_item_name = ttk.Label(popup, text="Nome do Item:")
        lbl_item_name.pack(pady=5)
        
        item_name_var = tk.StringVar()
        entry_item_name = ttk.Entry(popup, textvariable=item_name_var, width=25)
        entry_item_name.pack(pady=5)
        
        def submit():
            selected_code = code_var.get()
            if not selected_code:
                messagebox.showerror("Erro", "Selecione um código de item.")
                return
            
            # Extrai o código (antes do " - ")
            item_code = selected_code.split(" - ")[0]
            item_name = item_name_var.get().strip()
            if not item_name:
                messagebox.showerror("Erro", "Digite o nome do item.")
                return
            
            user_name = self.user[1]  # Nome do usuário logado
            location = self.user[5]
            department = self.user[6]
            
            add_stockroom_item(item_code, item_name, user_name, location, department)
            messagebox.showinfo("Sucesso", "Item cadastrado com sucesso.")
            popup.destroy()
            self.search_items()
        
        btn_submit = ttk.Button(popup, text="Cadastrar", command=submit, style="Small.TButton", width=10)
        btn_submit.pack(pady=10)
