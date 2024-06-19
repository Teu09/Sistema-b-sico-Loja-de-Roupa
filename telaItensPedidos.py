from tkinter import *
from tkinter import messagebox, ttk
from conexao import *

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Cadastro de Itens do Pedido")
        self.msg["font"] = ("verdana", "20", "bold")
        self.msg.pack()

        self.container2 = Frame(master)
        self.container2.pack()
        self.pedido = Label(self.container2, text="ID do Pedido")
        self.pedido.pack(side=LEFT)
        self.pedidoCombobox = ttk.Combobox(self.container2)
        self.pedidoCombobox.pack(side=RIGHT)

        self.container3 = Frame(master)
        self.container3.pack()
        self.produto = Label(self.container3, text="Produto")
        self.produto.pack(side=LEFT)
        self.produtoCombobox = ttk.Combobox(self.container3)
        self.produtoCombobox.pack(side=RIGHT)

        self.container4 = Frame(master)
        self.container4.pack()
        self.quantidade = Label(self.container4, text="Quantidade")
        self.quantidade.pack(side=LEFT)
        self.quantidadeEntry = Entry(self.container4)
        self.quantidadeEntry.pack(side=RIGHT)

        self.container5 = Frame(master)
        self.container5.pack()
        self.preco_unitario = Label(self.container5, text="Preço Unitário")
        self.preco_unitario.pack(side=LEFT)
        self.preco_unitarioEntry = Entry(self.container5)
        self.preco_unitarioEntry.pack(side=RIGHT)

        self.container6 = Frame(master)
        self.container6.pack()
        self.valor_total = Label(self.container6, text="Valor Total")
        self.valor_total.pack(side=LEFT)
        self.valor_totalEntry = Entry(self.container6, state='readonly')
        self.valor_totalEntry.pack(side=RIGHT)

        self.container7 = Frame(master)
        self.container7.pack()
        self.BtCalcular = Button(self.container7, text='Calcular Total', command=self.calcularTotal)
        self.BtCalcular.pack(side=LEFT)
        self.BtOk = Button(self.container7, text='Cadastrar', command=self.cadItemPedido)
        self.BtOk.pack(side=RIGHT)

        self.populateComboboxes()

    def populateComboboxes(self):
        mycursor = self.conexao.cursor()
        mycursor.execute("SELECT pedido_id FROM Pedidos")
        pedidos = mycursor.fetchall()
        self.pedidoCombobox['values'] = [pedido[0] for pedido in pedidos]

        mycursor.execute("SELECT produto_id, nome FROM Produtos")
        produtos = mycursor.fetchall()
        self.produtoCombobox['values'] = [produto[1] for produto in produtos]
        self.produtos_dict = {produto[1]: produto[0] for produto in produtos}
        mycursor.close()

    def calcularTotal(self):
        try:
            quantidade = int(self.quantidadeEntry.get())
            preco_unitario = float(self.preco_unitarioEntry.get())
            valor_total = quantidade * preco_unitario
            self.valor_totalEntry.config(state='normal')
            self.valor_totalEntry.delete(0, END)
            self.valor_totalEntry.insert(0, f"{valor_total:.2f}")
            self.valor_totalEntry.config(state='readonly')
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos para quantidade e preço unitário")

    def cadItemPedido(self, event=None):
        pedido_id = self.pedidoCombobox.get()
        produto_nome = self.produtoCombobox.get()
        produto_id = self.produtos_dict[produto_nome]
        quantidade = int(self.quantidadeEntry.get())
        preco_unitario = float(self.preco_unitarioEntry.get())
        preco_total = float(self.valor_totalEntry.get())

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'INSERT INTO Itens_Pedido (pedido_id, produto_id, quantidade, preco_unitario, preco_total) VALUES (%s, %s, %s, %s, %s)', 
            (pedido_id, produto_id, quantidade, preco_unitario, preco_total)
        )
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Item do pedido cadastrado com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''