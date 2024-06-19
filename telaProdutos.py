from tkinter import *
from tkinter import messagebox, ttk
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()
        
        self.msg = Label(self.container1, text="Cadastro de Produtos")
        self.msg["font"] = ("verdana", "20", "bold")
        self.msg.pack()

        self.container2 = Frame(self.container1)
        self.container2.pack(padx=10, pady=5)
        self.nome = Label(self.container2, text="Nome")
        self.nome.pack(side=LEFT)
        self.nomeEntry = Entry(self.container2)
        self.nomeEntry.pack(side=RIGHT)

        self.container3 = Frame(self.container1)
        self.container3.pack(padx=10, pady=5)
        self.descricao = Label(self.container3, text="Descrição")
        self.descricao.pack(side=LEFT)
        self.descricaoEntry = Entry(self.container3)
        self.descricaoEntry.pack(side=RIGHT)

        self.container4 = Frame(self.container1)
        self.container4.pack(padx=10, pady=5)
        self.preco = Label(self.container4, text="Preço")
        self.preco.pack(side=LEFT)
        self.precoEntry = Entry(self.container4)
        self.precoEntry.pack(side=RIGHT)

        self.container5 = Frame(self.container1)
        self.container5.pack(padx=10, pady=5)
        self.quantidade = Label(self.container5, text="Quantidade em Estoque")
        self.quantidade.pack(side=LEFT)
        self.quantidadeEntry = Entry(self.container5)
        self.quantidadeEntry.pack(side=RIGHT)

        self.container6 = Frame(self.container1)
        self.container6.pack(padx=10, pady=5)
        self.categoria = Label(self.container6, text="Categoria")
        self.categoria.pack(side=LEFT)
        self.categoriaCombobox = ttk.Combobox(self.container6)
        self.categoriaCombobox.pack(side=RIGHT)

        self.container7 = Frame(self.container1)
        self.container7.pack(padx=10, pady=5)
        self.fornecedor = Label(self.container7, text="Fornecedor")
        self.fornecedor.pack(side=LEFT)
        self.fornecedorCombobox = ttk.Combobox(self.container7)
        self.fornecedorCombobox.pack(side=RIGHT)

        self.container8 = Frame(self.container1)
        self.container8.pack(padx=10, pady=5)
        self.tamanho = Label(self.container8, text="Tamanho")
        self.tamanho.pack(side=LEFT)
        self.tamanhoCombobox = ttk.Combobox(self.container8)
        self.tamanhoCombobox.pack(side=RIGHT)

        self.container9 = Frame(self.container1)
        self.container9.pack(padx=10, pady=5)
        self.marca = Label(self.container9, text="Marca")
        self.marca.pack(side=LEFT)
        self.marcaCombobox = ttk.Combobox(self.container9)
        self.marcaCombobox.pack(side=RIGHT)

        self.container10 = Frame(self.container1)
        self.container10.pack(pady=10)
        self.BtOk = Button(self.container10, text='Cadastrar', command=self.cadProduto)
        self.BtOk.pack()

        self.populateComboboxes()

    def populateComboboxes(self):
        mycursor = self.conexao.cursor()

        mycursor.execute("SELECT categoria_id, nome FROM Categorias")
        categorias = mycursor.fetchall()
        self.categoriaCombobox['values'] = [categoria[1] for categoria in categorias]
        self.categorias_dict = {categoria[1]: categoria[0] for categoria in categorias}

        mycursor.execute("SELECT fornecedor_id, nome FROM Fornecedores")
        fornecedores = mycursor.fetchall()
        self.fornecedorCombobox['values'] = [fornecedor[1] for fornecedor in fornecedores]
        self.fornecedores_dict = {fornecedor[1]: fornecedor[0] for fornecedor in fornecedores}

        mycursor.execute("SELECT tamanho_id, descricao FROM Tamanhos")
        tamanhos = mycursor.fetchall()
        self.tamanhoCombobox['values'] = [tamanho[1] for tamanho in tamanhos]
        self.tamanhos_dict = {tamanho[1]: tamanho[0] for tamanho in tamanhos}

        mycursor.execute("SELECT marca_id, nome FROM Marcas")
        marcas = mycursor.fetchall()
        self.marcaCombobox['values'] = [marca[1] for marca in marcas]
        self.marcas_dict = {marca[1]: marca[0] for marca in marcas}

        mycursor.close()

    def cadProduto(self, event=None):
        nome = self.nomeEntry.get()
        descricao = self.descricaoEntry.get()
        preco = float(self.precoEntry.get())
        quantidade = int(self.quantidadeEntry.get())
        categoria_nome = self.categoriaCombobox.get()
        fornecedor_nome = self.fornecedorCombobox.get()
        tamanho_desc = self.tamanhoCombobox.get()
        marca_nome = self.marcaCombobox.get()

        categoria_id = self.categorias_dict[categoria_nome]
        fornecedor_id = self.fornecedores_dict[fornecedor_nome]
        tamanho_id = self.tamanhos_dict[tamanho_desc]
        marca_id = self.marcas_dict[marca_nome]

        mycursor = self.conexao.cursor()
        mycursor.execute(
            'INSERT INTO Produtos (nome, descricao, preco, quantidade_estoque, categoria_id, fornecedor_id, tamanho_id, marca_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
            (nome, descricao, preco, quantidade, categoria_id, fornecedor_id, tamanho_id, marca_id)
        )
        
        self.conexao.commit()
        mycursor.close()

        messagebox.showinfo('Sucesso', 'Produto cadastrado com sucesso')

'''root = Tk()
Application(root)
root.mainloop()'''