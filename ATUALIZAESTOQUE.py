from tkinter import *
from tkinter import messagebox, ttk
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Atualização de Estoque")
        self.msg["font"] = ("verdana", "20", "bold")
        self.msg.pack()

        self.container2 = Frame(master)
        self.container2.pack()
        self.produto = Label(self.container2, text="Produto")
        self.produto.pack(side=LEFT)
        self.produtoCombobox = ttk.Combobox(self.container2, width=30)
        self.produtoCombobox.pack(side=RIGHT)

        self.container3 = Frame(master)
        self.container3.pack()
        self.fornecedor = Label(self.container3, text="Fornecedor")
        self.fornecedor.pack(side=LEFT)
        self.fornecedorCombobox = ttk.Combobox(self.container3, width=30)
        self.fornecedorCombobox.pack(side=RIGHT)

        self.container4 = Frame(master)
        self.container4.pack()
        self.categoria = Label(self.container4, text="Categoria")
        self.categoria.pack(side=LEFT)
        self.categoriaCombobox = ttk.Combobox(self.container4, width=30)
        self.categoriaCombobox.pack(side=RIGHT)

        self.container5 = Frame(master)
        self.container5.pack()
        self.marca = Label(self.container5, text="Marca")
        self.marca.pack(side=LEFT)
        self.marcaCombobox = ttk.Combobox(self.container5, width=30)
        self.marcaCombobox.pack(side=RIGHT)

        self.container6 = Frame(master)
        self.container6.pack()
        self.tamanho = Label(self.container6, text="Tamanho")
        self.tamanho.pack(side=LEFT)
        self.tamanhoCombobox = ttk.Combobox(self.container6, width=30)
        self.tamanhoCombobox.pack(side=RIGHT)

        self.container7 = Frame(master)
        self.container7.pack()
        self.quantidade = Label(self.container7, text="Nova Quantidade em Estoque")
        self.quantidade.pack(side=LEFT)
        self.quantidadeEntry = Entry(self.container7)
        self.quantidadeEntry.pack(side=RIGHT)

        self.container8 = Frame(master)
        self.container8.pack()
        self.quantidade_atual_label = Label(self.container8, text="Quantidade Atual em Estoque:")
        self.quantidade_atual_label.pack(side=LEFT)
        self.quantidade_atual_entry = Entry(self.container8, state='readonly')
        self.quantidade_atual_entry.pack(side=RIGHT)

        self.container9 = Frame(master)
        self.container9.pack()
        self.BtOk = Button(self.container9, text='Atualizar', command=self.atualizaEstoque)
        self.BtOk.pack()

        self.populateComboboxes()

    def populateComboboxes(self):
        mycursor = self.conexao.cursor()
        mycursor.execute("SELECT produto_id, nome, quantidade_estoque FROM Produtos")
        produtos = mycursor.fetchall()
        self.produtoCombobox['values'] = [produto[1] for produto in produtos]
        self.produtos_dict = {produto[1]: (produto[0], produto[2]) for produto in produtos}

        mycursor.execute("SELECT fornecedor_id, nome FROM Fornecedores")
        fornecedores = mycursor.fetchall()
        self.fornecedorCombobox['values'] = [fornecedor[1] for fornecedor in fornecedores]
        self.fornecedores_dict = {fornecedor[1]: fornecedor[0] for fornecedor in fornecedores}

        mycursor.execute("SELECT categoria_id, nome FROM Categorias")
        categorias = mycursor.fetchall()
        self.categoriaCombobox['values'] = [categoria[1] for categoria in categorias]
        self.categorias_dict = {categoria[1]: categoria[0] for categoria in categorias}

        mycursor.execute("SELECT marca_id, nome FROM Marcas")
        marcas = mycursor.fetchall()
        self.marcaCombobox['values'] = [marca[1] for marca in marcas]
        self.marcas_dict = {marca[1]: marca[0] for marca in marcas}

        mycursor.execute("SELECT tamanho_id, descricao FROM Tamanhos")
        tamanhos = mycursor.fetchall()
        self.tamanhoCombobox['values'] = [tamanho[1] for tamanho in tamanhos]
        self.tamanhos_dict = {tamanho[1]: tamanho[0] for tamanho in tamanhos}

        mycursor.close()

        self.produtoCombobox.bind("<<ComboboxSelected>>", self.update_quantidade_atual)

    def update_quantidade_atual(self, event=None):
        produto_nome = self.produtoCombobox.get()
        quantidade_atual = self.produtos_dict[produto_nome][1]
        self.quantidade_atual_entry.config(state=NORMAL)
        self.quantidade_atual_entry.delete(0, END)
        self.quantidade_atual_entry.insert(0, quantidade_atual)
        self.quantidade_atual_entry.config(state='readonly')

    def atualizaEstoque(self, event=None):
        produto_nome = self.produtoCombobox.get()
        nova_quantidade = int(self.quantidadeEntry.get())
        produto_id = self.produtos_dict[produto_nome][0]

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'UPDATE Produtos SET quantidade_estoque = %s WHERE produto_id = %s', 
            (nova_quantidade, produto_id)
        )
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Estoque atualizado com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''