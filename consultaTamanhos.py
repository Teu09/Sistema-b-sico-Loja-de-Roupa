from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Descrição'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Descrição')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.consultaTamanhos)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarTamanho)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarTamanho)
        self.botaoAtualizar.pack(side=LEFT)

    def consultaTamanhos(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('SELECT tamanho_id, descricao FROM Tamanhos')
        resultado = cursor.fetchall()

        for row in resultado:
            self.consulta.insert('', 'end', values=row)

    def deletarTamanho(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            tamanho_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Tamanhos WHERE tamanho_id = %s', (tamanho_id,))
            self.conexao.commit()
            self.consulta.delete(item)

    def atualizarTamanho(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione um tamanho para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Tamanho')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Descrição"]
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
            tamanho_id = novos_valores[0]
            cursor = self.conexao.cursor()
            cursor.execute("""UPDATE Tamanhos SET descricao = %s WHERE tamanho_id = %s""",
                           (novos_valores[1], tamanho_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_valores)
            janelaAtualizar.destroy()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)

'''root = Tk()
Application(root)
root.mainloop()'''