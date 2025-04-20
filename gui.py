import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from auth import register_user, login_user, validate_registration_fields
from DB.databaseConnect import connect
from PIL import Image, ImageTk

def login_window():
    """Initialize and display the main application window."""
    app = InventoryApp()
    app.mainloop()



class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.title("Inventory App")
        self.title("InventoryApp")

        self.iconbitmap(r"Icon\logo.ico")

        self.state("zoomed")  # Fullscreen
        self.configure(bg="#f0f4f8")

        self.resizable(True, True)
        self.minsize(600, 600)

        # Configura estilos
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Roboto", 12), foreground="#333")
        self.style.configure(
            "TButton",
            font=("Roboto", 12, "bold"),
            padding=10,
            background="#0078d7",
            foreground="#fff",
            borderwidth=0,
            focuscolor="#0056a1",
        )
        self.style.map(
            "TButton",
            background=[("active", "#0056a1"), ("pressed", "#004080")],
            foreground=[("active", "#fff"), ("pressed", "#fff")],
        )
        self.style.configure(
            "TEntry",
            font=("Roboto", 12),
            padding=5,
            relief="flat",
            fieldbackground="#fff",
            borderwidth=1,
            foreground="#333",
        )

        # Container principal
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Inicializa as páginas (frames)
        self.frames = {}
        for F in (LoginPage, RegisterPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.pack(fill="both", expand=True)
            frame.pack_forget()

        self.destroy_frame(LoginPage)
        self.destroy_frame(RegisterPage)
        self.show_frame(LoginPage)

    def create_frame(self, frame_class):
        """Cria uma nova instância do frame, armazena no dicionário e retorna-o."""
        frame = frame_class(self.container, self)
        self.frames[frame_class] = frame
        return frame
    
    def destroy_frame(self, frame_class):
        """Destrói a instância do frame e remove do dicionário."""
        if frame_class in self.frames:
            self.frames[frame_class].destroy()
            del self.frames[frame_class]

    def show_frame(self, page):
        """Exibe o frame desejado."""
        # Se o frame não existir (foi destruído), recria-o.
        if page not in self.frames:
            self.create_frame(page)
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[page].pack(fill="both", expand=True)

    def show_menu(self, user):
        from menu import MenuScreen
        # Se já existir uma tela de Menu, destrua-a para recriar com os dados atuais
        if MenuScreen in self.frames:
            self.frames[MenuScreen].destroy()
        menu_frame = MenuScreen(self.container, self, user)
        self.frames[MenuScreen] = menu_frame
        self.show_frame(MenuScreen)

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame", padding=20)
        image = Image.open("Imagens\logo.png")  # Ex: assets/logo.png
        image = image.resize((80, 100))  # Redimensiona se quiser
        self.photo = ImageTk.PhotoImage(image)

        # Container centralizado
        container = ttk.Frame(self)
        container.pack(expand=True)
        container.pack_propagate(False)
        container.configure(width=400, height=550)

        image_label = ttk.Label(container, image=self.photo)
        image_label.pack(pady=(0, 0))
        # Título
        ttk.Label(container, text="Login", font=("Roboto", 24, "bold")).pack(pady=(10, 20))

        # Variáveis de entrada
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Campo Email
        ttk.Label(container, text="Email:", font=("Roboto", 12)).pack(anchor="w", padx=10)
        self.email_entry = ttk.Entry(container, textvariable=self.email_var)
        self.email_entry.pack(padx=10, pady=5, fill="x")
        self.email_entry.insert(0, "Type your email")
        self.email_entry.config(foreground="#aaa")
        self.email_entry.bind("<FocusIn>", self.on_email_focus_in)
        self.email_entry.bind("<FocusOut>", self.on_email_focus_out)
        self.email_entry.focus_set()

        # Campo Password
        ttk.Label(container, text="Password:", font=("Roboto", 12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.password_entry = ttk.Entry(container, textvariable=self.password_var, show="*")
        self.password_entry.pack(padx=10, pady=5, fill="x")
        self.password_entry.insert(0, "Type your password")
        self.password_entry.config(foreground="#aaa")
        self.password_entry.bind("<FocusIn>", self.on_password_focus_in)
        self.password_entry.bind("<FocusOut>", self.on_password_focus_out)

        # Mensagem de erro/sucesso
        self.message_label = ttk.Label(container, text="")
        self.message_label.pack(pady=10)

        # Botões
        ttk.Button(container, text="Login", command=self.login).pack(pady=5, ipadx=20)
        ttk.Button(container, text="Register", command=self.go_to_register).pack(pady=5, ipadx=20)
        ttk.Button(container, text="Forgot my password", command=self.forgot_password, style="Small.TButton", width=12).pack(pady=5)


    def on_email_focus_in(self, event):
        if self.email_entry.get() == "Type your email":
            self.email_entry.delete(0, tk.END)
            self.email_entry.config(foreground="#333")

    def on_email_focus_out(self, event):
        if not self.email_entry.get():
            self.email_entry.insert(0, "Type your email")
            self.email_entry.config(foreground="#aaa")

    def on_password_focus_in(self, event):
        if self.password_entry.get() == "Type your password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(foreground="#333")

    def on_password_focus_out(self, event):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Type your password")
            self.password_entry.config(foreground="#aaa")

    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()
        user = login_user(email, password)

        if user:
            self.message_label.config(text="Login successful!", foreground="green")
            self.controller.show_menu(user)
        else:
            self.message_label.config(text="Invalid email or password.", foreground="red")

    def go_to_register(self):
        # Destrói a instância atual de LoginPage
        self.controller.destroy_frame(LoginPage)
        # Mostra a tela de Register (se já não existir, ela será recriada em show_frame)
        self.controller.show_frame(RegisterPage)

    def forgot_password(self):
        popup = tk.Toplevel(self)
        popup.title("Recover your password")
        tk.Label(popup, text="Type your e-mail:").pack(pady=5)
        email_var = tk.StringVar()
        ttk.Entry(popup, textvariable=email_var).pack(pady=5)
        def send():
            from auth import send_password_reset
            ok = send_password_reset(email_var.get())
            msg = "Recover e-mail sent" if ok else "E-mail not found"
            tk.Label(popup, text=msg).pack(pady=5)
        ttk.Button(popup, text="Send", command=send).pack(pady=10)


class RegisterPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame", padding=20)

        # Container centralizado
        container = ttk.Frame(self)
        container.pack(expand=True)
        container.pack_propagate(False)
        container.configure(width=400, height=600)

        # Título
        ttk.Label(container, text="Register", font=("Roboto", 24, "bold")).pack(pady=10)

        # Variáveis dos campos
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.continent_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.department_var = tk.StringVar()

        # Campo Name
        ttk.Label(container, text="Name:", font=("Roboto", 12)).pack(anchor="w", pady=5)
        self.name_entry = ttk.Entry(container, textvariable=self.name_var)
        self.name_entry.pack(pady=5, fill="x")
        self.setup_placeholder(self.name_entry, "Type your name")
        self.name_entry.focus_set()

        # Campo Email
        ttk.Label(container, text="Email:", font=("Roboto", 12)).pack(anchor="w", pady=5)
        self.email_entry = ttk.Entry(container, textvariable=self.email_var)
        self.email_entry.pack(pady=5, fill="x")
        self.setup_placeholder(self.email_entry, "Type your email")

        # Campo Password
        ttk.Label(container, text="Password:", font=("Roboto", 12)).pack(anchor="w", pady=5)
        self.password_entry = ttk.Entry(container, textvariable=self.password_var, show="*")
        self.password_entry.pack(pady=5, fill="x")
        self.setup_placeholder(self.password_entry, "Type your password")

        # Combobox de Continent
        ttk.Label(container, text="Continent:", font=("Roboto", 12)).pack(anchor="w", pady=5)
        self.continent_combobox = ttk.Combobox(container, textvariable=self.continent_var, state="readonly")
        self.continent_combobox.pack(pady=5, fill="x")
        self.continent_combobox.bind("<<ComboboxSelected>>", self.update_locations)
        self.setup_placeholder(self.continent_combobox, "Select your Global Location")
        
        # Combobox de Location
        ttk.Label(container, text="Location:", font=("Roboto", 12)).pack(anchor="w", pady=5)
        self.location_combobox = ttk.Combobox(container, textvariable=self.location_var, state="readonly")
        self.location_combobox.pack(pady=5, fill="x")
        self.location_combobox.bind("<<ComboboxSelected>>", lambda event: None)
        self.setup_placeholder(self.location_combobox, "Select your Local Location")

        # Combobox de Department
        ttk.Label(container, text="Department:", font=("Roboto", 12)).pack(anchor="w", pady=5)
        self.department_combobox = ttk.Combobox(container, textvariable=self.department_var, state="readonly")
        self.department_combobox.pack(pady=5, fill="x")
        self.department_combobox.bind("<<ComboboxSelected>>", lambda event: None)
        self.setup_placeholder(self.department_combobox, "Select your Department")

        # Popula os combobox de continentes e departamentos
        self.populate_continents()
        self.populate_departments()

        # Label para mensagens
        self.message_label = ttk.Label(container, text="")
        self.message_label.pack(pady=0)

        self.unblock_fields()
        self.clear_fields()

        # Botões
        ttk.Button(container, text="Confirm", command=self.confirm).pack(pady=5, fill="x")
        ttk.Button(container, text="Back", command=self.back).pack(pady=5, fill="x")

    def setup_placeholder(self, entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.config(foreground="#aaa")

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(foreground="#333")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(foreground="#aaa")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def clear_fields(self):
        self.name_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.continent_var.set("")
        self.location_var.set("")
        self.department_var.set("")
        self.setup_placeholder(self.name_entry, "Type your name")
        self.setup_placeholder(self.email_entry, "Type your email")
        self.setup_placeholder(self.password_entry, "Type your password")
        self.setup_placeholder(self.continent_combobox, "Select your Global Location")
        self.setup_placeholder(self.location_combobox, "Select your Local Location")
        self.setup_placeholder(self.department_combobox, "Select your Department")
        self.message_label.config(text="")

    def block_fields(self):
        self.name_entry.config(state="disabled")
        self.email_entry.config(state="disabled")
        self.password_entry.config(state="disabled")
        self.continent_combobox.config(state="disabled")
        self.location_combobox.config(state="disabled")
        self.department_combobox.config(state="disabled")

    def unblock_fields(self):
        self.name_entry.config(state="normal")
        self.email_entry.config(state="normal")
        self.password_entry.config(state="normal")
        self.continent_combobox.config(state="normal")
        self.location_combobox.config(state="normal")
        self.department_combobox.config(state="normal")

    def confirm(self):
        name = self.name_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        continent = self.continent_var.get()
        location = self.location_var.get()
        department = self.department_var.get()

        # Valida os campos
        is_valid, message = validate_registration_fields(name, email, password, continent, location, department)
        if not is_valid:
            self.message_label.config(text=message, foreground="red")
            return

        # Realiza o registro
        status, result_message = register_user(name, email, password, continent, location, department)
        self.message_label.config(
            text=result_message,
            foreground="green" if status == "success" else "red",
        )

        if status == "success":
            self.block_fields()
            self.message_label.config(
                text="Verify your e-mail to activate your account",
                foreground="green"
            )

    def back(self):
        # Destrói a instância atual de RegisterPage
        self.controller.destroy_frame(RegisterPage)
        # Recria uma nova instância de LoginPage
        self.controller.create_frame(LoginPage)
        self.controller.show_frame(LoginPage)

    def populate_continents(self):
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name FROM continents ORDER BY name;")
                continents = cursor.fetchall()
                self.continent_combobox['values'] = [continent[1] for continent in continents]
                if continents:
                    self.continent_combobox.current(0)
                    self.populate_locations()

    def populate_locations(self):
        continent = self.continent_var.get()
        with connect() as conn:
            with conn.cursor() as cursor:
                if continent:
                    cursor.execute("""
                    SELECT locations.city_name
                    FROM locations
                    JOIN continents ON locations.continent_id = continents.id
                    WHERE continents.name = %s
                    ORDER BY locations.city_name;
                    """, (continent,))
                else:
                    cursor.execute("SELECT city_name FROM locations ORDER BY city_name;")
                locations = cursor.fetchall()
                self.location_combobox['values'] = [location[0] for location in locations]
                if locations:
                    self.location_combobox.current(0)

    def update_locations(self, event=None):
        self.populate_locations()

    def update_continent(self, event=None):
        location = self.location_var.get()
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT continents.name
                FROM locations
                JOIN continents ON locations.continent_id = continents.id
                WHERE locations.city_name = %s;
                """, (location,))
                result = cursor.fetchone()
                if result:
                    self.continent_combobox.set(result[0])

    def populate_departments(self):
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name FROM departments ORDER BY name;")
                departments = cursor.fetchall()
                self.department_combobox['values'] = [dept[1] for dept in departments]
                if departments:
                    self.department_combobox.current(0)
