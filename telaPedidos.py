from tkinter import *
from tkinter import messagebox, ttk
from conexao import *

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Cadastro de Pedidos")
        self.msg["font"] = ("verdana", "20", "bold")
        self.msg.pack()

        self.container2 = Frame(master)
        self.container2.pack()
        self.cliente = Label(self.container2, text="Cliente")
        self.cliente.pack(side=LEFT)
        self.clienteCombobox = ttk.Combobox(self.container2)
        self.clienteCombobox.pack(side=RIGHT)

        self.container3 = Frame(master)
        self.container3.pack()
        self.data = Label(self.container3, text="Data")
        self.data.pack(side=LEFT)
        self.dataEntry = Entry(self.container3)
        self.dataEntry.pack(side=RIGHT)

        self.container4 = Frame(master)
        self.container4.pack()
        self.valor_total = Label(self.container4, text="Valor Total")
        self.valor_total.pack(side=LEFT)
        self.valor_totalEntry = Entry(self.container4)
        self.valor_totalEntry.pack(side=RIGHT)

        self.container5 = Frame(master)
        self.container5.pack()
        self.forma_pagamento = Label(self.container5, text="Forma de Pagamento")
        self.forma_pagamento.pack(side=LEFT)
        self.formaPagamentoCombobox = ttk.Combobox(self.container5)
        self.formaPagamentoCombobox.pack(side=RIGHT)

        self.container6 = Frame(master)
        self.container6.pack()
        self.BtOk = Button(self.container6, text='Cadastrar', command=self.cadPedido)
        self.BtOk.pack()

        self.populateComboboxes()

    def populateComboboxes(self):
        mycursor = self.conexao.cursor()
        mycursor.execute("SELECT cliente_id, nome FROM Clientes")
        clientes = mycursor.fetchall()
        self.clienteCombobox['values'] = [cliente[1] for cliente in clientes]
        self.clientes_dict = {cliente[1]: cliente[0] for cliente in clientes}

        mycursor.execute("SELECT forma_pagamento_id, descricao FROM Formas_Pagamento")
        formas_pagamento = mycursor.fetchall()
        self.formaPagamentoCombobox['values'] = [forma[1] for forma in formas_pagamento]
        self.formas_pagamento_dict = {forma[1]: forma[0] for forma in formas_pagamento}

        mycursor.close()

    def cadPedido(self, event=None):
        cliente_nome = self.clienteCombobox.get()
        cliente_id = self.clientes_dict[cliente_nome]
        data = self.dataEntry.get()
        valor_total = float(self.valor_totalEntry.get())
        forma_pagamento_desc = self.formaPagamentoCombobox.get()
        forma_pagamento_id = self.formas_pagamento_dict[forma_pagamento_desc]

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'INSERT INTO Pedidos (cliente_id, data_pedido, valor_total, forma_pagamento_id) VALUES (%s, %s, %s, %s)',
            (cliente_id, data, valor_total, forma_pagamento_id)
        )
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Pedido cadastrado com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''