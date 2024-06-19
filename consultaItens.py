from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Pedido ID', 'Produto', 'Quantidade', 'Preço Unitário', 'Preço Total'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Pedido ID')
        self.consulta.heading('#3', text='Produto')
        self.consulta.heading('#4', text='Quantidade')
        self.consulta.heading('#5', text='Preço Unitário')
        self.consulta.heading('#6', text='Preço Total')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.consultaItensPedido)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarItemPedido)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarItemPedido)
        self.botaoAtualizar.pack(side=LEFT)

    def consultaItensPedido(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('''
            SELECT i.item_id, i.pedido_id, p.nome, i.quantidade, i.preco_unitario, i.preco_total
            FROM Itens_Pedido i
            JOIN Produtos p ON i.produto_id = p.produto_id
        ''')
        resultado = cursor.fetchall()

        for row in resultado:
            self.consulta.insert('', 'end', values=row)

    def deletarItemPedido(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            item_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Itens_Pedido WHERE item_id = %s', (item_id,))
            self.conexao.commit()
            self.consulta.delete(item)

    def atualizarItemPedido(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione um item de pedido para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Item de Pedido')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Pedido ID", "Produto", "Quantidade", "Preço Unitário", "Preço Total"]
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
            novos_valores = [entry.get() for entry in entries]
            item_id = novos_valores[0]
            pedido_id = novos_valores[1]
            produto_nome = novos_valores[2]
            quantidade = novos_valores[3]
            preco_unitario = novos_valores[4]
            preco_total = novos_valores[5]

            cursor = self.conexao.cursor()
            cursor.execute('SELECT produto_id FROM Produtos WHERE nome = %s', (produto_nome,))
            produto_id = cursor.fetchone()[0]

            cursor.execute('''
                UPDATE Itens_Pedido
                SET pedido_id = %s, produto_id = %s, quantidade = %s, preco_unitario = %s, preco_total = %s
                WHERE item_id = %s
            ''', (pedido_id, produto_id, quantidade, preco_unitario, preco_total, item_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_valores)
            janelaAtualizar.destroy()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)


'''root = Tk()
Application(root)
root.mainloop()'''