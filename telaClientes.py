from tkinter import *
from tkinter import messagebox
from conexao import *

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
        self.nome = Label(self.container2, text="Nome")
        self.nome.pack(side=LEFT)
        self.nomeEntry = Entry(self.container2)
        self.nomeEntry.pack(side=RIGHT)

        self.container3 = Frame(master)
        self.container3.pack()
        self.email = Label(self.container3, text="Email")
        self.email.pack(side=LEFT)
        self.emailEntry = Entry(self.container3)
        self.emailEntry.pack(side=RIGHT)

        self.container4 = Frame(master)
        self.container4.pack()
        self.endereco = Label(self.container4, text="Endereço")
        self.endereco.pack(side=LEFT)
        self.enderecoEntry = Entry(self.container4)
        self.enderecoEntry.pack(side=RIGHT)

        self.container5 = Frame(master)
        self.container5.pack()
        self.cidade = Label(self.container5, text="Cidade")
        self.cidade.pack(side=LEFT)
        self.cidadeEntry = Entry(self.container5)
        self.cidadeEntry.pack(side=RIGHT)

        self.container6 = Frame(master)
        self.container6.pack()
        self.estado = Label(self.container6, text="Estado")
        self.estado.pack(side=LEFT)
        self.estadoEntry = Entry(self.container6)
        self.estadoEntry.pack(side=RIGHT)

        self.container7 = Frame(master)
        self.container7.pack()
        self.cep = Label(self.container7, text="CEP")
        self.cep.pack(side=LEFT)
        self.cepEntry = Entry(self.container7)
        self.cepEntry.pack(side=RIGHT)

        self.container8 = Frame(master)
        self.container8.pack()
        self.BtOk = Button(self.container8, text='Cadastrar', command=self.cadUsuario)
        self.BtOk.pack()

    def cadUsuario(self, event=None):
        nome = self.nomeEntry.get()
        email = self.emailEntry.get()
        endereco = self.enderecoEntry.get()
        cidade = self.cidadeEntry.get()
        estado = self.estadoEntry.get()
        cep = self.cepEntry.get()

        mycursor = self.conexao.cursor()
        mycursor.execute('INSERT INTO Clientes (nome, email, endereco, cidade, estado, cep, data_criacao) VALUES (%s, %s, %s, %s, %s, %s, CURDATE())', 
                         (nome, email, endereco, cidade, estado, cep))
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Operação realizada com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''