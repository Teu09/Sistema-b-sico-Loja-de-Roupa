from tkinter import *
from tkinter import messagebox, ttk
from conexao import *

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Cadastro de Marcas")
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
        self.BtOk = Button(self.container3, text='Cadastrar', command=self.cadMarca)
        self.BtOk.pack()

    def cadMarca(self, event=None):
        nome = self.nomeEntry.get()

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'INSERT INTO Marcas (nome) VALUES (%s)', 
            (nome,)
        )
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Marca cadastrada com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''