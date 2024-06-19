from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Nome', 'Contato', 'Email', 'Endereço', 'Cidade', 'Estado', 'CEP'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Nome')
        self.consulta.heading('#3', text='Contato')
        self.consulta.heading('#4', text='Email')
        self.consulta.heading('#5', text='Endereço')
        self.consulta.heading('#6', text='Cidade')
        self.consulta.heading('#7', text='Estado')
        self.consulta.heading('#8', text='CEP')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.ConsultaFornecedores)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarFornecedor)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarFornecedor)
        self.botaoAtualizar.pack(side=LEFT)

    def ConsultaFornecedores(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('SELECT fornecedor_id, nome, contato, email, endereco, cidade, estado, cep FROM Fornecedores')
        resultado = cursor.fetchall()

        for row in resultado:
            self.consulta.insert('', 'end', values=row)

    def deletarFornecedor(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            fornecedor_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Fornecedores WHERE fornecedor_id = %s', (fornecedor_id,))
            self.conexao.commit()
            self.consulta.delete(item)

    def atualizarFornecedor(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione um fornecedor para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Fornecedor')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Nome", "Contato", "Email", "Endereço", "Cidade", "Estado", "CEP"]
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
            fornecedor_id = novos_Valores[0]
            cursor = self.conexao.cursor()
            cursor.execute("""UPDATE Fornecedores SET nome = %s, contato = %s, email = %s, endereco = %s, cidade = %s, estado = %s, cep = %s WHERE fornecedor_id = %s""",
                           (novos_Valores[1], novos_Valores[2], novos_Valores[3], novos_Valores[4], novos_Valores[5], novos_Valores[6], novos_Valores[7], fornecedor_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_Valores)
            janelaAtualizar.destroy()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)


'''root = Tk()
Application(root)
root.mainloop()'''