from tkinter import *
from tkinter import messagebox, ttk
from conexao import *

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Cadastro de Tamanhos")
        self.msg["font"] = ("verdana", "20", "bold")
        self.msg.pack()

        self.container2 = Frame(master)
        self.container2.pack()
        self.descricao = Label(self.container2, text="Descrição")
        self.descricao.pack(side=LEFT)
        self.descricaoEntry = Entry(self.container2)
        self.descricaoEntry.pack(side=RIGHT)

        self.container3 = Frame(master)
        self.container3.pack()
        self.BtOk = Button(self.container3, text='Cadastrar', command=self.cadTamanho)
        self.BtOk.pack()

    def cadTamanho(self, event=None):
        descricao = self.descricaoEntry.get()

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'INSERT INTO Tamanhos (descricao) VALUES (%s)', 
            (descricao,)
        )
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Tamanho cadastrado com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''