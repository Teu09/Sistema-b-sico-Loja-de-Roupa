from tkinter import *
from tkinter.ttk import Treeview, Combobox
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Cliente', 'Usuário', 'Senha', 'Data de Criação'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Cliente')
        self.consulta.heading('#3', text='Usuário')
        self.consulta.heading('#4', text='Senha')
        self.consulta.heading('#5', text='Data de Criação')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.ConsultaLogins)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarLogin)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarLogin)
        self.botaoAtualizar.pack(side=LEFT)

    def ConsultaLogins(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('SELECT login_id, cliente_id, usuario, senha, data_criacao FROM Logins')
        resultado = cursor.fetchall()

        for row in resultado:
            login_id, cliente_id, usuario, senha, data_criacao = row
            
            cursor.execute('SELECT nome FROM Clientes WHERE cliente_id = %s', (cliente_id,))
            cliente_nome = cursor.fetchone()[0]

            self.consulta.insert('', 'end', values=(login_id, cliente_nome, usuario, senha, data_criacao))

        cursor.close()

    def deletarLogin(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            login_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Logins WHERE login_id = %s', (login_id,))
            self.conexao.commit()
            self.consulta.delete(item)
            cursor.close()

    def atualizarLogin(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione um login para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Login')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Cliente", "Usuário", "Senha", "Data de Criação"]
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
            else:
                entry = Entry(frame)
                entry.insert(0, value)
                entry.pack(side=LEFT, fill=X, expand=True)
                entries.append(entry)

        def atualizar():
            novos_Valores = [entry.get() for entry in entries]
            login_id = novos_Valores[0]
            
            cursor = self.conexao.cursor()
            cursor.execute('SELECT cliente_id FROM Clientes WHERE nome = %s', (novos_Valores[1],))
            cliente_id = cursor.fetchone()[0]
            
            cursor.execute("""UPDATE Logins SET cliente_id = %s, usuario = %s, senha = %s, data_criacao = %s WHERE login_id = %s""",
                           (cliente_id, novos_Valores[2], novos_Valores[3], novos_Valores[4], login_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_Valores)
            janelaAtualizar.destroy()
            cursor.close()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)

'''root = Tk()
Application(root)
root.mainloop()'''