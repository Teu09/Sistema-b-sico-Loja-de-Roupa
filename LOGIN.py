from tkinter import *
from tkinter import messagebox
from conexao import *
from PIL import Image, ImageTk
import home

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.configure(bg='black')

        self.img = Image.open("C:/FACUL_ESUP/Virtual_Projeto/LogoTrabalho.png")
        self.img = ImageTk.PhotoImage(self.img)

        self.background_frame = Frame(master, bg='black')
        self.background_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.canvas = Canvas(self.background_frame, width=self.img.width(), height=self.img.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        self.frame_login = Frame(self.background_frame, bg='black')
        self.frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.label_username = Label(self.frame_login, text="Usuário:", bg='black', fg='white')
        self.label_username.pack(pady=5)
        self.entry_username = Entry(self.frame_login)
        self.entry_username.pack(pady=5)

        self.label_password = Label(self.frame_login, text="Senha:", bg='black', fg='white')
        self.label_password.pack(pady=5)
        self.entry_password = Entry(self.frame_login, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = Button(self.frame_login, text="Login", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        cursor = conexao.cursor()
        cursor.execute('SELECT cliente_id FROM Logins WHERE usuario = %s AND senha = %s', (username, password))
        resultado = cursor.fetchone()

        if resultado:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.master.destroy()
            home.iniciar_home()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

root = Tk()
root.geometry("1024x1024")
app = Application(root)
root.mainloop()