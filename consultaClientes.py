from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Nome', 'Email', 'Endereço', 'Cidade', 'Estado', 'CEP', 'Data de Criação'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Nome')
        self.consulta.heading('#3', text='Email')
        self.consulta.heading('#4', text='Endereço')
        self.consulta.heading('#5', text='Cidade')
        self.consulta.heading('#6', text='Estado')
        self.consulta.heading('#7', text='CEP')
        self.consulta.heading('#8', text='Data de Criação')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.ConsultaClientes)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarCliente)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarCliente)
        self.botaoAtualizar.pack(side=LEFT)

    def ConsultaClientes(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('SELECT cliente_id, nome, email, endereco, cidade, estado, cep, data_criacao FROM Clientes')
        resultado = cursor.fetchall()

        for row in resultado:
            self.consulta.insert('', 'end', values=row)

    def deletarCliente(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            cliente_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Clientes WHERE cliente_id = %s', (cliente_id,))
            self.conexao.commit()
            self.consulta.delete(item)

    def atualizarCliente(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione um cliente para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Cliente')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Nome", "Email", "Endereço", "Cidade", "Estado", "CEP", "Data de Criação"]
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
            cliente_id = novos_Valores[0]
            cursor = self.conexao.cursor()
            cursor.execute("""UPDATE Clientes SET nome = %s, email = %s, endereco = %s, cidade = %s, estado = %s, cep = %s, data_criacao = %s WHERE cliente_id = %s""",
                           (novos_Valores[1], novos_Valores[2], novos_Valores[3], novos_Valores[4], novos_Valores[5], novos_Valores[6], novos_Valores[7], cliente_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_Valores)
            janelaAtualizar.destroy()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)


'''root = Tk()
Application(root)
root.mainloop()'''