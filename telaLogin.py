from tkinter import *
from tkinter import messagebox, ttk
from conexao import *
from datetime import datetime 

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Cadastro de Usuários")
        self.msg["font"] = ("verdana", "20", "bold")
        self.msg.pack()

        self.container2 = Frame(master)
        self.container2.pack()
        self.usuario = Label(self.container2, text="Usuário")
        self.usuario.pack(side=LEFT)
        self.usuarioEntry = Entry(self.container2)
        self.usuarioEntry.pack(side=RIGHT)

        self.container3 = Frame(master)
        self.container3.pack()
        self.senha = Label(self.container3, text="Senha")
        self.senha.pack(side=LEFT)
        self.senhaEntry = Entry(self.container3, show="*")
        self.senhaEntry.pack(side=RIGHT)

        self.container5 = Frame(master)
        self.container5.pack()
        self.cliente = Label(self.container5, text="Cliente")
        self.cliente.pack(side=LEFT)
        self.clienteCombobox = ttk.Combobox(self.container5)
        self.clienteCombobox.pack(side=RIGHT)

        self.container6 = Frame(master)
        self.container6.pack()
        self.BtOk = Button(self.container6, text='Cadastrar', command=self.cadUsuario)
        self.BtOk.pack()

        self.populateComboboxes()

    def populateComboboxes(self):
        mycursor = self.conexao.cursor()
        mycursor.execute("SELECT cliente_id, nome FROM Clientes")
        clientes = mycursor.fetchall()
        self.clienteCombobox['values'] = [cliente[1] for cliente in clientes]
        self.clientes_dict = {cliente[1]: cliente[0] for cliente in clientes}
        mycursor.close()

    def cadUsuario(self, event=None):
        usuario = self.usuarioEntry.get()
        senha = self.senhaEntry.get()
        data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cliente_nome = self.clienteCombobox.get()
        cliente_id = self.clientes_dict[cliente_nome]

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'INSERT INTO Logins (cliente_id, usuario, senha, data_criacao) VALUES (%s, %s, %s, %s)', 
            (cliente_id, usuario, senha, data_criacao)
        )
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''