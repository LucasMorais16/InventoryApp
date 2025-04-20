# menu.py
import tkinter as tk
from tkinter import ttk
from gui import LoginPage
from InventoryScreen import InventoryScreen
from PIL import Image, ImageTk  # Importa as classes do Pillow
from Checklist import ChecklistTemplateScreen

class MenuScreen(ttk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.pack(fill="both", expand=True)
        
        # Barra lateral
        self.sidebar = tk.Frame(self, bg="#d9e1f2", width=400)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        department = user[6] + " - " + user[5] if len(user) > 6 else "Department"
        dept_label = tk.Label(self.sidebar, text=department, bg="#d9e1f2", font=("Roboto", 16, "bold"))
        dept_label.pack(pady=20)

        btn_home = ttk.Button(self.sidebar, text="Home", command=self.open_home)
        btn_home.pack(pady=10, padx=20, fill="x")
        
        btn_checklist = ttk.Button(self.sidebar, text="Checklist", command=self.open_checklist)
        btn_checklist.pack(pady=10, padx=20, fill="x")
        
        btn_inventory = ttk.Button(self.sidebar, text="Inventory", command=self.open_inventory)
        btn_inventory.pack(pady=10, padx=20, fill="x")
        
        spacer = tk.Frame(self.sidebar, bg="#d9e1f2")
        spacer.pack(expand=True, fill="both")
        
        btn_exit = ttk.Button(self.sidebar, text="Exit", command=self.exit_menu)
        btn_exit.pack(pady=10, padx=20, fill="x")
        
        # Área principal
        self.content_area = tk.Frame(self, bg="#f0f4f8")
        self.content_area.pack(side="left", fill="both", expand=True)
        self.open_home()
    
    def open_home(self):
        # Limpa a área de conteúdo antes de inserir novos widgets
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # --- Carregar e exibir a imagem utilizando Pillow ---
        try:
            # Abre a imagem do arquivo; ajuste o caminho conforme necessário
            image = Image.open("Imagens\logo.png")
            # Redimensiona a imagem para um tamanho pequeno, se desejar (80x80 pode ser ajustado)
            image = image.resize((120, 150))
            # Converte a imagem para um objeto compatível com tkinter
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            # Caso ocorra algum erro na leitura da imagem, exibe uma mensagem e finaliza
            print(f"Erro ao carregar imagem: {e}")
            photo = None

        if photo:
            logo_image_label = tk.Label(self.content_area, image=photo, bg="#f0f4f8")
            # Guarde uma referência à imagem para evitar que ela seja coletada pelo garbage collector
            logo_image_label.image = photo
            logo_image_label.pack(pady=(20, 10))
        
        
        info_text = (
            "Program Info and Contacts:\n"
            "Email: lucas.santoslima.morais@hotmail.com\n"
        )
        info_label = tk.Label(self.content_area, text=info_text, bg="#f0f4f8", font=("Roboto", 12))
        info_label.pack(pady=10)

    def open_checklist(self):
        # Remove widgets atuais na área de conteúdo
        for widget in self.content_area.winfo_children():
            widget.destroy()
        # Insere a tela de templates de checklist e define o callback
        ChecklistTemplateScreen(
            self.content_area,
            self.user,
            on_template_selected=self.open_checklist_instances
        )

    def open_checklist_instances(self, template_id):
       # limpa área
        for widget in self.content_area.winfo_children():
            widget.destroy() 
        # importa aqui para não criar dependência circular
        from Checklist import ChecklistInstanceScreen
        ChecklistInstanceScreen(
            self.content_area,
            self.user,
            template_id,
            on_back=self.open_checklist  # volta para a lista de templates
        )
    
    def open_inventory(self):
        # Remove widgets atuais na área de conteúdo
        for widget in self.content_area.winfo_children():
            widget.destroy()
        # Insere a tela de inventário
        InventoryScreen(self.content_area, self.user)
    
    def exit_menu(self):
        self.controller.destroy_frame(MenuScreen)
        self.controller.destroy_frame(InventoryScreen)
        self.controller.create_frame(LoginPage)
        self.controller.show_frame(LoginPage)
