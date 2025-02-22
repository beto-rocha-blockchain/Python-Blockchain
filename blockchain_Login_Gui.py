import tkinter as tk
from tkinter import messagebox
import re

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Blockchain")
        self.root.geometry("300x300")
        
        # Simulação de dados de usuários
        self.users = {
            'admin': {
                'password': 'adminpass',
                'email': 'admin@example.com',
                'phone': '+123456789'
            },
            'user': {
                'password': 'userpass',
                'email': 'user@example.com',
                'phone': '+987654321'
            }
        }
        
        # Criar interface de login
        self.create_login_interface()

    def create_login_interface(self):
        # Rótulos e campos de entrada
        tk.Label(self.root, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Botão de login
        tk.Button(self.root, text="Login", command=self.authenticate).pack(pady=20)

        # Botão para criar novo usuário
        tk.Button(self.root, text="Criar Novo Usuário", command=self.create_user_window).pack(pady=10)

    @staticmethod
    def send_email_confirmation(email):
        print(f"E-mail de confirmação enviado para {email}.")
        return True

    @staticmethod
    def send_sms_confirmation(phone):
        print(f"Mensagem de texto enviada para {phone}.")
        return True

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.users.get(username)
        if user and user['password'] == password:
            if self.send_email_confirmation(user['email']) and self.send_sms_confirmation(user['phone']):
                messagebox.showinfo("Sucesso", "Login confirmado com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha na verificação de e-mail ou SMS.")
        else:
            messagebox.showerror("Erro", "Login ou senha incorretos.")

    def create_user_window(self):
        self.create_user_window = tk.Toplevel(self.root)
        self.create_user_window.title("Criar Novo Usuário")

        tk.Label(self.create_user_window, text="Novo Usuário:").pack(pady=5)
        self.new_username_entry = tk.Entry(self.create_user_window)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.create_user_window, text="Nova Senha:").pack(pady=5)
        self.new_password_entry = tk.Entry(self.create_user_window, show="*")
        self.new_password_entry.pack(pady=5)

        tk.Label(self.create_user_window, text="E-mail:").pack(pady=5)
        self.new_email_entry = tk.Entry(self.create_user_window)
        self.new_email_entry.pack(pady=5)

        tk.Label(self.create_user_window, text="Telefone:").pack(pady=5)
        self.new_phone_entry = tk.Entry(self.create_user_window)
        self.new_phone_entry.pack(pady=5)

        tk.Button(self.create_user_window, text="Criar", command=self.on_create_user).pack(pady=20)

    def on_create_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        new_email = self.new_email_entry.get()
        new_phone = self.new_phone_entry.get()

        if not self.is_strong_password(new_password):
            messagebox.showerror("Erro", "A senha deve ter pelo menos 8 caracteres, incluir letras maiúsculas, minúsculas, números e caracteres especiais.")
            return

        if new_username in self.users:
            messagebox.showerror("Erro", "Usuário já existe.")
        else:
            self.users[new_username] = {
                'password': new_password,
                'email': new_email,
                'phone': new_phone
            }
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
            self.create_user_window.destroy()

    @staticmethod
    def is_strong_password(password):
        if len(password) < 8:
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        if not re.search(r'[\"!@#$%¨&*()_+\-=/\*+,.;:~^´`\[\]{}<>\\|ºª¿]', password):
            return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()