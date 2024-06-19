from tkinter import *
from tkinter.ttk import Treeview, Combobox
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Cliente', 'Data do Pedido', 'Valor Total', 'Forma de Pagamento'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Cliente')
        self.consulta.heading('#3', text='Data do Pedido')
        self.consulta.heading('#4', text='Valor Total')
        self.consulta.heading('#5', text='Forma de Pagamento')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.ConsultaPedidos)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarPedido)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarPedido)
        self.botaoAtualizar.pack(side=LEFT)

    def ConsultaPedidos(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('SELECT pedido_id, cliente_id, data_pedido, valor_total, forma_pagamento_id FROM Pedidos')
        resultado = cursor.fetchall()

        for row in resultado:
            pedido_id, cliente_id, data_pedido, valor_total, forma_pagamento_id = row
            
            cursor.execute('SELECT nome FROM Clientes WHERE cliente_id = %s', (cliente_id,))
            cliente_nome = cursor.fetchone()[0]
            
            cursor.execute('SELECT descricao FROM Formas_Pagamento WHERE forma_pagamento_id = %s', (forma_pagamento_id,))
            forma_pagamento_descricao = cursor.fetchone()[0]

            self.consulta.insert('', 'end', values=(pedido_id, cliente_nome, data_pedido, valor_total, forma_pagamento_descricao))

        cursor.close()

    def deletarPedido(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            pedido_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Pedidos WHERE pedido_id = %s', (pedido_id,))
            self.conexao.commit()
            self.consulta.delete(item)
            cursor.close()

    def atualizarPedido(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione um pedido para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Pedido')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Cliente", "Data do Pedido", "Valor Total", "Forma de Pagamento"]
        entries = []

        for i, (label_text, value) in enumerate(zip(labels, values)):
            frame = Frame(janelaAtualizar)
            frame.pack(fill=X, padx=10, pady=5)
            label = Label(frame, text=label_text, width=20, anchor=W)
            label.pack(side=LEFT)

            if label_text == 'Cliente':
                cursor = self.conexao.cursor()
                cursor.execute('SELECT cliente_id, nome FROM Clientes')
                clientes = cursor.fetchall()
                cursor.close()
                cliente_nomes = [cliente[1] for cliente in clientes]

                entry = Combobox(frame, values=cliente_nomes)
                entry.set(value)
                entry.pack(side=LEFT, fill=X, expand=True)
                entries.append(entry)
            elif label_text == 'Forma de Pagamento':
                cursor = self.conexao.cursor()
                cursor.execute('SELECT forma_pagamento_id, descricao FROM Formas_Pagamento')
                formas_pagamento = cursor.fetchall()
                cursor.close()
                pagamento_descricoes = [pagamento[1] for pagamento in formas_pagamento]

                entry = Combobox(frame, values=pagamento_descricoes)
                entry.set(value)
                entry.pack(side=LEFT, fill=X, expand=True)
                entries.append(entry)
            else:
                entry = Entry(frame)
                entry.insert(0, value)
                entry.pack(side=LEFT, fill=X, expand=True)
                entries.append(entry)

        def atualizar():
            novos_Valores = [entry.get() for entry in entries]
            pedido_id = novos_Valores[0]
            
            cursor = self.conexao.cursor()
            cursor.execute('SELECT cliente_id FROM Clientes WHERE nome = %s', (novos_Valores[1],))
            cliente_id = cursor.fetchone()[0]
            
            cursor.execute('SELECT forma_pagamento_id FROM Formas_Pagamento WHERE descricao = %s', (novos_Valores[4],))
            forma_pagamento_id = cursor.fetchone()[0]
            
            cursor.execute("""UPDATE Pedidos SET cliente_id = %s, data_pedido = %s, valor_total = %s, forma_pagamento_id = %s WHERE pedido_id = %s""",
                           (cliente_id, novos_Valores[2], novos_Valores[3], forma_pagamento_id, pedido_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_Valores)
            janelaAtualizar.destroy()
            cursor.close()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)

'''root = Tk()
Application(root)
root.mainloop()'''