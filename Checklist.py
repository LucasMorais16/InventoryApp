import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Import database functions
from DB.databaseConnect import connect
from DB.database_checklist_template import (
    get_all_templates,
    add_new_template,
    get_template_by_id
)
from DB.database_checklist import (
    get_checklists_for_template,
    add_new_checklist
)

class ChecklistTemplateScreen(ttk.Frame):
    """
    Tela para listagem e criação de templates de checklist
    """
    def __init__(self, parent, user, on_template_selected):
        super().__init__(parent)
        self.user = user
        self.on_template_selected = on_template_selected
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_templates()

    def create_widgets(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.btn_new = ttk.Button(top, text="New template", command=self.open_new_template_popup)
        self.btn_new.pack(side="left")

        # List of templates
        self.tree = ttk.Treeview(self, columns=("id", "title"), show="headings")
        self.tree.heading("title", text="Template Title")
        self.tree.column("id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind('<Double-1>', self.template_double_clicked)

    def load_templates(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        templates = get_all_templates()
        for tpl in templates:
            # tpl: (id, title)
            self.tree.insert("", "end", values=(tpl[0], tpl[1]))

    def open_new_template_popup(self):
        popup = tk.Toplevel(self)
        popup.title("New Checklist Template")
        popup.geometry("400x350")

        ttk.Label(popup, text="Template Title:").pack(pady=5)
        title_var = tk.StringVar()
        ttk.Entry(popup, textvariable=title_var, width=40).pack(pady=5)

        ttk.Label(popup, text="Checklist Items (one per line):").pack(pady=5)
        items_text = tk.Text(popup, height=10, width=45)
        items_text.pack(pady=5)

        def submit():
            title = title_var.get().strip()
            items = [line.strip() for line in items_text.get("1.0", tk.END).splitlines() if line.strip()]
            if not title or not items:
                messagebox.showerror("Error", "Title and at least one checklist item are required.")
                return
            # Save template
            add_new_template(title, items, self.user[0])
            messagebox.showinfo("Success", "Template created successfully.")
            popup.destroy()
            self.load_templates()

        ttk.Button(popup, text="Create", command=submit).pack(pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack()

    def template_double_clicked(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        tpl_id, _ = self.tree.item(sel[0], 'values')
        self.on_template_selected(tpl_id)


class ChecklistInstanceScreen(ttk.Frame):
    """
    Tela para listagem e criação de checklists de um template específico
    """
    def __init__(self, parent, user, template_id, on_back):
        super().__init__(parent)
        self.user = user
        self.template_id = template_id
        self.on_back = on_back
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_checklists()

    def create_widgets(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.btn_back = ttk.Button(top, text="Back", command=self.on_back)
        self.btn_back.pack(side="left")

        self.btn_new = ttk.Button(top, text="New checklist", command=self.open_new_checklist_popup)
        self.btn_new.pack(side="left", padx=5)

        # Columns: equipment, recipient, created by, created at
        cols = ("id", "equipment", "recipient", "user", "created_at")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.heading("equipment", text="Equipment")
        self.tree.heading("recipient", text="Recipient")
        self.tree.heading("user", text="Created By")
        self.tree.heading("created_at", text="Created At")
        self.tree.column("id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_checklists(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        items = get_checklists_for_template(self.template_id)
        for chk in items:
            # chk: (id, equipment, recipient, created_by, created_date)
            created_str = chk[4].strftime("%Y-%m-%d %H:%M:%S")
            self.tree.insert(
                "", "end",
                values=(chk[0], chk[1], chk[2], chk[3], created_str)
            )

    def open_new_checklist_popup(self):
        tpl = get_template_by_id(self.template_id)

        popup = tk.Toplevel(self)
        popup.title(f"New Checklist - {tpl['title']}")
        popup.geometry("400x600")

        # Input for equipment and recipient
        ttk.Label(popup, text="Equipment Name:").pack(pady=5)
        equipment_var = tk.StringVar()
        ttk.Entry(popup, textvariable=equipment_var, width=40).pack(pady=5)

        ttk.Label(popup, text="Recipient Name:").pack(pady=5)
        recipient_var = tk.StringVar()
        ttk.Entry(popup, textvariable=recipient_var, width=40).pack(pady=5)

        ttk.Label(popup, text="Checklist Items:").pack(pady=5)
        item_vars = []
        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True, pady=5)
        for idx, item in enumerate(tpl['items'], start=1):
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(frame, text=item, variable=var)
            chk.pack(anchor="w")
            item_vars.append((item, var))

        def submit():
            equipment = equipment_var.get().strip()
            recipient = recipient_var.get().strip()
            if not equipment or not recipient:
                messagebox.showerror("Error", "Equipment and Recipient are required.")
                return
            results = {item: var.get() for item, var in item_vars}
            add_new_checklist(self.template_id, self.user[1], equipment, recipient, results)
            messagebox.showinfo("Success", "Checklist saved successfully.")
            popup.destroy()
            self.load_checklists()

        ttk.Button(popup, text="Save", command=submit).pack(side="left", padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack(side="left", padx=10)