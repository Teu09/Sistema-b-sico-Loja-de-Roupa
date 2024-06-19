from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Nome', 'Descrição', 'Preço', 'Quantidade em Estoque', 'Categoria', 'Fornecedor', 'Marca', 'Tamanho'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Nome')
        self.consulta.heading('#3', text='Descrição')
        self.consulta.heading('#4', text='Preço')
        self.consulta.heading('#5', text='Quantidade em Estoque')
        self.consulta.heading('#6', text='Categoria')
        self.consulta.heading('#7', text='Fornecedor')
        self.consulta.heading('#8', text='Marca')
        self.consulta.heading('#9', text='Tamanho')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.ConsultaProdutos)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarProduto)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarProduto)
        self.botaoAtualizar.pack(side=LEFT)

    def ConsultaProdutos(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('''
            SELECT p.produto_id, p.nome, p.descricao, p.preco, p.quantidade_estoque, 
                   c.nome AS categoria, f.nome AS fornecedor, m.nome AS marca, t.descricao AS tamanho
            FROM Produtos p
            JOIN Categorias c ON p.categoria_id = c.categoria_id
            JOIN Fornecedores f ON p.fornecedor_id = f.fornecedor_id
            JOIN Marcas m ON p.marca_id = m.marca_id
            JOIN Tamanhos t ON p.tamanho_id = t.tamanho_id
        ''')
        resultado = cursor.fetchall()

        for row in resultado:
            self.consulta.insert('', 'end', values=row)

    def deletarProduto(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            produto_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Produtos WHERE produto_id = %s', (produto_id,))
            self.conexao.commit()
            self.consulta.delete(item)

    def atualizarProduto(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione um produto para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Produto')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Nome", "Descrição", "Preço", "Quantidade em Estoque", "Categoria", "Fornecedor", "Marca", "Tamanho"]
        entries = []

        for i, (label_text, value) in enumerate(zip(labels, values)):
            frame = Frame(janelaAtualizar)
            frame.pack(fill=X, padx=10, pady=5)
            label = Label(frame, text=label_text, width=20, anchor=W)
            label.pack(side=LEFT)
            entry = Entry(frame)
            entry.insert(0, value)
            entry.pack(side=LEFT, fill=X, expand=True)
            entries.append(entry)

        def atualizar():
            novos_Valores = [entry.get() for entry in entries]
            produto_id = novos_Valores[0]
            cursor = self.conexao.cursor()
            cursor.execute("""UPDATE Produtos SET nome = %s, descricao = %s, preco = %s, quantidade_estoque = %s WHERE produto_id = %s""",
                           (novos_Valores[1], novos_Valores[2], novos_Valores[3], novos_Valores[4], produto_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_Valores)
            janelaAtualizar.destroy()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)

'''root = Tk()
Application(root)
root.mainloop()'''