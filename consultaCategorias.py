from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
from conexao import conexao

class Application:
    def __init__(self, master=None):
        self.conexao = conexao
        
        self.container1 = Frame(master)
        self.container1.pack()

        self.consulta = Treeview(master, columns=('ID', 'Nome', 'Descrição'), show='headings', height=10)
        self.consulta.heading('#1', text='ID')
        self.consulta.heading('#2', text='Nome')
        self.consulta.heading('#3', text='Descrição')
        self.consulta.pack()

        self.botaoConsulta = Button(master, text='Consultar', command=self.ConsultaCategorias)
        self.botaoConsulta.pack(side=LEFT)

        self.botaoDeletar = Button(master, text='Deletar', command=self.deletarCategoria)
        self.botaoDeletar.pack(side=RIGHT)
        
        self.botaoAtualizar = Button(master, text='Atualizar', command=self.atualizarCategoria)
        self.botaoAtualizar.pack(side=LEFT)

    def ConsultaCategorias(self):
        self.consulta.delete(*self.consulta.get_children())

        cursor = self.conexao.cursor()
        cursor.execute('SELECT categoria_id, nome, descricao FROM Categorias')
        resultado = cursor.fetchall()

        for row in resultado:
            self.consulta.insert('', 'end', values=row)

    def deletarCategoria(self):
        selecionados = self.consulta.selection()

        for item in selecionados:
            categoria_id = self.consulta.item(item, 'values')[0]
            cursor = self.conexao.cursor()
            cursor.execute('DELETE FROM Categorias WHERE categoria_id = %s', (categoria_id,))
            self.conexao.commit()
            self.consulta.delete(item)

    def atualizarCategoria(self):
        selected_item = self.consulta.focus()
        if not selected_item:
            messagebox.showwarning('Aviso', 'Selecione uma categoria para atualizar.')
            return

        janelaAtualizar = Toplevel()
        janelaAtualizar.title('Atualizar Categoria')

        values = self.consulta.item(selected_item, "values")
        
        labels = ["ID", "Nome", "Descrição"]
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
            categoria_id = novos_Valores[0]
            cursor = self.conexao.cursor()
            cursor.execute("""UPDATE Categorias SET nome = %s, descricao = %s WHERE categoria_id = %s""",
                           (novos_Valores[1], novos_Valores[2], categoria_id))
            self.conexao.commit()
            self.consulta.item(selected_item, values=novos_Valores)
            janelaAtualizar.destroy()

        atualizar_button = Button(janelaAtualizar, text="Atualizar", command=atualizar)
        atualizar_button.pack(pady=10)


'''root = Tk()
Application(root)
root.mainloop()'''