from tkinter import *
import tkinter as tk
from conexao import *  
import telaCategorias
import telaItensPedidos
import telaLogin
import telaPagamentos
import telaPedidos
import telaProdutos
import telaTelefones
import telaClientes
import telaFornecedor
import consultaCategorias
import consultaItens
import consultaLogin
import consultaPagamentos
import consultaPedidos
import consultaProdutos
import consultaTelefones
import consultaClientes
import consultaFornecedor
import VENDA
import ATUALIZAESTOQUE
from PIL import Image, ImageTk
import telaMarcas
import consultaMarcas
import telaTamanhos
import consultaTamanhos

class Application:
    def __init__(self, master=None):
        self.master = master
        self.img = Image.open("C:/FACUL_ESUP/Virtual_Projeto/LogoTrabalho.png")
        self.img = ImageTk.PhotoImage(self.img)
        self.background_frame = Frame(master, bg='black')
        self.background_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas = Canvas(self.background_frame, width=self.img.width(), height=self.img.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        menubar = tk.Menu(master)

        cadastro_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Cadastro', menu=cadastro_menu)
        cadastro_menu.add_command(label='Categorias', command=self.cadastrarCategorias)
        cadastro_menu.add_command(label='Itens', command=self.cadastrarItens)
        cadastro_menu.add_command(label='Login', command=self.cadastrarLogin)
        cadastro_menu.add_command(label='Pagamentos', command=self.cadastrarPagamentos)
        cadastro_menu.add_command(label='Pedidos', command=self.cadastrarPedidos)
        cadastro_menu.add_command(label='Produtos', command=self.cadastrarProdutos)
        cadastro_menu.add_command(label='Telefones', command=self.cadastrarTelefones)
        cadastro_menu.add_command(label='Clientes', command=self.cadastrarClientes)
        cadastro_menu.add_command(label='Fornecedores', command=self.cadastrarFornecedores)
        cadastro_menu.add_command(label='Marcas',command=self.cadastrarMarcas)
        cadastro_menu.add_command(label='Tamanhos',command=self.cadastrarTamanhos)
        master.config(menu=menubar)

        consulta_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Consulta', menu=consulta_menu)
        consulta_menu.add_command(label='Categorias', command=self.consultarCategorias)
        consulta_menu.add_command(label='Login', command=self.consultarLogin)
        consulta_menu.add_command(label='Pagamentos', command=self.consultarPagamentos)
        consulta_menu.add_command(label='Pedidos', command=self.consultarPedidos)
        consulta_menu.add_command(label='Produtos', command=self.consultarProdutos)
        consulta_menu.add_command(label='Telefones', command=self.consultarTelefones)
        consulta_menu.add_command(label='Clientes', command=self.consultarClientes)
        consulta_menu.add_command(label='Fornecedores', command=self.consultarFornecedores)
        consulta_menu.add_command(label='Marcas', command=self.consultarMarcas)
        consulta_menu.add_command(label='Tamanhos', command=self.consultarTamanhos)

        venda_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Vendas', menu=venda_menu)
        venda_menu.add_command(label='Venda', command=self.vendas)
        venda_menu.add_command(label='Itens', command=self.consultarItens)

        atlestoque = tk.Menu(menubar)
        menubar.add_cascade(label='Estoque', menu=atlestoque)
        atlestoque.add_command(label='Atualizar', command=self.atualizar_estoque)

    def vendas(self):
        novaJanela = Toplevel()
        VENDA.Application(novaJanela)

    def cadastrarCategorias(self):
        novaJanela = Toplevel()
        telaCategorias.Application(novaJanela)

    def cadastrarItens(self):
        novaJanela = Toplevel()
        telaItensPedidos.Application(novaJanela)

    def cadastrarLogin(self):
        novaJanela = Toplevel()
        telaLogin.Application(novaJanela)

    def cadastrarPagamentos(self):
        novaJanela = Toplevel()
        telaPagamentos.Application(novaJanela)

    def cadastrarPedidos(self):
        novaJanela = Toplevel()
        telaPedidos.Application(novaJanela)

    def cadastrarProdutos(self):
        novaJanela = Toplevel()
        telaProdutos.Application(novaJanela)

    def cadastrarTelefones(self):
        novaJanela = Toplevel()
        telaTelefones.Application(novaJanela)

    def cadastrarClientes(self):
        novaJanela = Toplevel()
        telaClientes.Application(novaJanela)

    def cadastrarFornecedores(self):
        novaJanela = Toplevel()
        telaFornecedor.Application(novaJanela)

    def consultarCategorias(self):
        novaJanela = Toplevel()
        consultaCategorias.Application(novaJanela)

    def consultarItens(self):
        novaJanela = Toplevel()
        consultaItens.Application(novaJanela)

    def consultarLogin(self):
        novaJanela = Toplevel()
        consultaLogin.Application(novaJanela)

    def consultarPagamentos(self):
        novaJanela = Toplevel()
        consultaPagamentos.Application(novaJanela)

    def consultarPedidos(self):
        novaJanela = Toplevel()
        consultaPedidos.Application(novaJanela)

    def consultarProdutos(self):
        novaJanela = Toplevel()
        consultaProdutos.Application(novaJanela)

    def consultarTelefones(self):
        novaJanela = Toplevel()
        consultaTelefones.Application(novaJanela)

    def consultarClientes(self):
        novaJanela = Toplevel()
        consultaClientes.Application(novaJanela)

    def consultarFornecedores(self):
        novaJanela = Toplevel()
        consultaFornecedor.Application(novaJanela)

    def atualizar_estoque(self):
        novaJanela = Toplevel()
        ATUALIZAESTOQUE.Application(novaJanela)

    def cadastrarMarcas(self):
        novaJanela = Toplevel()
        telaMarcas.Application(novaJanela)

    def consultarMarcas(self):
        novaJanela = Toplevel()
        consultaMarcas.Application(novaJanela)

    def consultarTamanhos(self):
        novaJanela = Toplevel()
        consultaTamanhos.Application(novaJanela)

    def cadastrarTamanhos(self):
        novaJanela = Toplevel()
        telaTamanhos.Application(novaJanela)

def iniciar_home():
    root = Tk()
    root.geometry("1024x1024")
    app = Application(root)
    root.mainloop()