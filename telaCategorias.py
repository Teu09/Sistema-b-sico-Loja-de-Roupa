from tkinter import *
from tkinter import messagebox
from conexao import *

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Cadastro de Categorias")
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
        self.descricao = Label(self.container3, text="Descrição")
        self.descricao.pack(side=LEFT)
        self.descricaoEntry = Entry(self.container3)
        self.descricaoEntry.pack(side=RIGHT)

        self.container4 = Frame(master)
        self.container4.pack()
        self.BtOk = Button(self.container4, text='Cadastrar', command=self.cadCategoria)
        self.BtOk.pack()

    def cadCategoria(self, event=None):
        nome = self.nomeEntry.get()
        descricao = self.descricaoEntry.get()

        mycursor = self.conexao.cursor()
        mycursor.execute('INSERT INTO Categorias (nome, descricao) VALUES (%s, %s)', (nome, descricao))
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Categoria cadastrada com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''