from tkinter import *
from tkinter import messagebox, ttk
from conexao import conexao
from datetime import datetime

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        self.container1 = Frame(master)
        self.container1.pack()
        self.msg = Label(self.container1, text="Ponto de Venda")
        self.msg["font"] = ("verdana", "20", "bold")
        self.msg.pack()

        self.container2 = Frame(master)
        self.container2.pack()
        self.cliente_label = Label(self.container2, text="Cliente")
        self.cliente_label.pack(side=LEFT)

        mycursor = self.conexao.cursor()
        mycursor.execute("SELECT cliente_id, nome FROM Clientes")
        clientes = mycursor.fetchall()
        mycursor.close()

        self.cliente_id_map = {cliente[1]: cliente[0] for cliente in clientes}
        nome_cliente = [cliente[1] for cliente in clientes]

        self.cliente_combo = ttk.Combobox(self.container2, values=nome_cliente)
        self.cliente_combo.pack(side=LEFT, padx=10, pady=5)

        self.container3 = Frame(master)
        self.container3.pack()
        self.produto = Label(self.container3, text="Produto")
        self.produto.pack(side=LEFT)

        mycursor = self.conexao.cursor()
        mycursor.execute("SELECT produto_id, nome, preco FROM Produtos")
        produtos = mycursor.fetchall()
        mycursor.close()

        self.produto_id_map = {produto[1]: (produto[0], produto[2]) for produto in produtos}
        nome_produto = [produto[1] for produto in produtos]

        self.produto_combo = ttk.Combobox(self.container3, values=nome_produto)
        self.produto_combo.pack(side=LEFT, padx=10, pady=5)
        self.produto_combo.bind("<<ComboboxSelected>>", self.update_preco_unitario_base)

        self.container4 = Frame(master)
        self.container4.pack()
        self.quantidade_label = Label(self.container4, text="Quantidade")
        self.quantidade_label.pack(side=LEFT)
        self.quantidade_entry = Entry(self.container4)
        self.quantidade_entry.pack(side=RIGHT)

        self.container5 = Frame(master)
        self.container5.pack()
        self.preco_unitario_base_label = Label(self.container5, text="Preço Base")
        self.preco_unitario_base_label.pack(side=LEFT)
        self.preco_unitario_base_entry = Entry(self.container5, state='readonly')
        self.preco_unitario_base_entry.pack(side=RIGHT)

        self.container6 = Frame(master)
        self.container6.pack()
        self.preco_label = Label(self.container6, text="Preço de Venda")
        self.preco_label.pack(side=LEFT)
        self.preco_entry = Entry(self.container6)
        self.preco_entry.pack(side=RIGHT)


        self.container7 = Frame(master)
        self.container7.pack()
        self.total_label = Label(self.container7, text="Total")
        self.total_label.pack(side=LEFT)
        self.total_entry = Entry(self.container7, state='readonly')
        self.total_entry.pack(side=RIGHT)

        self.container8 = Frame(master)
        self.container8.pack()
        self.pagamento_label = Label(self.container8, text="Forma de Pagamento")
        self.pagamento_label.pack(side=LEFT)

        mycursor = self.conexao.cursor()
        mycursor.execute("SELECT forma_pagamento_id, descricao FROM Formas_Pagamento")
        formas_pagamento = mycursor.fetchall()
        mycursor.close()

        self.pagamento_id_map = {pagamento[1]: pagamento[0] for pagamento in formas_pagamento}
        descricao_pagamento = [pagamento[1] for pagamento in formas_pagamento]

        self.pagamento_combo = ttk.Combobox(self.container8, values=descricao_pagamento)
        self.pagamento_combo.pack(side=LEFT, padx=10, pady=5)

        self.container9 = Frame(master)
        self.container9.pack()
        self.BtOk = Button(self.container9, text='Finalizar Venda', command=self.finalizar_venda)
        self.BtOk.pack()

        self.quantidade_entry.bind("<KeyRelease>", self.update_total)
        self.preco_entry.bind("<KeyRelease>", self.update_total)

    def update_preco_unitario_base(self, event=None):
        nome_produto = self.produto_combo.get()
        produto_id, preco_base = self.produto_id_map[nome_produto]

        self.preco_unitario_base_entry.config(state=NORMAL)
        self.preco_unitario_base_entry.delete(0, END)
        self.preco_unitario_base_entry.insert(0, f"{preco_base:.2f}")
        self.preco_unitario_base_entry.config(state='readonly')

        self.preco_entry.delete(0, END)
        self.preco_entry.insert(0, f"{preco_base:.2f}")

    def update_total(self, event=None):
        try:
            quantidade = int(self.quantidade_entry.get())
            preco_unitario = float(self.preco_entry.get())
            total = quantidade * preco_unitario
            self.total_entry.config(state=NORMAL)
            self.total_entry.delete(0, END)
            self.total_entry.insert(0, f"{total:.2f}")
            self.total_entry.config(state='readonly')
        except ValueError:
            self.total_entry.config(state=NORMAL)
            self.total_entry.delete(0, END)
            self.total_entry.config(state='readonly')

    def finalizar_venda(self):
        nome_cliente = self.cliente_combo.get()
        nome_produto = self.produto_combo.get()
        quantidade = int(self.quantidade_entry.get())
        preco_unitario = float(self.preco_entry.get())
        total = quantidade * preco_unitario

        cliente_id = self.cliente_id_map.get(nome_cliente)
        produto_id = self.produto_id_map.get(nome_produto)[0]
        forma_pagamento_desc = self.pagamento_combo.get()
        forma_pagamento_id = self.pagamento_id_map.get(forma_pagamento_desc)
        data_pedido = datetime.now().strftime('%Y-%m-%d')

        with open('vendas.txt', 'a') as file:
            file.write(f"Cliente: {nome_cliente}\n")
            file.write(f"Produto: {nome_produto}\n")
            file.write(f"Quantidade: {quantidade}\n")
            file.write(f"Preço Unitário: {preco_unitario:.2f}\n")
            file.write(f"Total: {total:.2f}\n")
            file.write(f"Forma de Pagamento: {forma_pagamento_desc}\n")
            file.write(f"Data do Pedido: {data_pedido}\n\n")

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'INSERT INTO Pedidos (cliente_id, data_pedido, valor_total, forma_pagamento_id) VALUES ( %s, %s, %s, %s)',
            (cliente_id, data_pedido, total, forma_pagamento_id)
        )
        pedido_id = mycursor.lastrowid
        self.conexao.commit()

        mycursor.execute(
            'INSERT INTO Itens_Pedido (pedido_id, produto_id, quantidade, preco_unitario, preco_total) VALUES (%s, %s, %s, %s, %s)',
            (pedido_id, produto_id, quantidade, preco_unitario, total)
        )
        self.conexao.commit()

        mycursor.execute(
            'UPDATE Produtos SET quantidade_estoque = quantidade_estoque - %s WHERE produto_id = %s',
            (quantidade, produto_id)
        )
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Venda registrada com sucesso.')

'''root = Tk()
Application(root)
root.mainloop()'''