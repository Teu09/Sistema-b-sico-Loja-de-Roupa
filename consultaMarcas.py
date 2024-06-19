from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Nome'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Nome')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.consultaMarcas)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarMarca)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarMarca)
        self.botaoAtualizar.pack(side=LEFT)

    def consultaMarcas(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('SELECT marca_id, nome FROM Marcas')
        resultado = cursor.fetchall()

        for row in resultado:
            self.consulta.insert('', 'end', values=row)

    def deletarMarca(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            marca_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Marcas WHERE marca_id = %s', (marca_id,))
            self.conexao.commit()
            self.consulta.delete(item)

    def atualizarMarca(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione uma marca para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Marca')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Nome"]
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
            marca_id = novos_valores[0]
            cursor = self.conexao.cursor()
            cursor.execute("""UPDATE Marcas SET nome = %s WHERE marca_id = %s""",
                           (novos_valores[1], marca_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_valores)
            janelaAtualizar.destroy()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)


'''root = Tk()
Application(root)
root.mainloop()'''