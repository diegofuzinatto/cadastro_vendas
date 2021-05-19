from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime

from venda import Venda

class Funcoes():
    def __init__(self, lb_cod_venda_content, cod_venda, nome_entry, data_entry, valor_entry, busca_entry, data_inicio_entry, data_fim_entry,
            lb_mensagem_1, lb_mensagem_2, listaVenda):
        self.lb_cod_venda_content = lb_cod_venda_content
        self.cod_venda = cod_venda
        self.nome_entry = nome_entry
        self.data_entry = data_entry
        self.valor_entry = valor_entry
        self.busca_entry = busca_entry
        self.data_inicio_entry = data_inicio_entry
        self.data_fim_entry = data_fim_entry
        self.lb_mensagem_1 = lb_mensagem_1
        self.lb_mensagem_2 = lb_mensagem_2
        self.listaVenda = listaVenda


    def select_lista(self):
        venda = Venda()

        lista = venda.select_lista()

        self.listaVenda.delete(*self.listaVenda.get_children())

        for row in lista:
            self.listaVenda.insert("", END, values=(row['cod_venda'], row['nome'], row['data'], row['valor']))

    def OnDoubleClick(self, event):
        self.limpa_tela()

        for n in self.listaVenda.selection():
            col1, col2, col3, col4 = self.listaVenda.item(n, 'values')
            self.lb_cod_venda_content.config(text=col1)
            self.nome_entry.insert(END, col2)
            self.data_entry.delete(0, END)
            self.data_entry.insert(END, col3)
            self.valor_entry.insert(END, col4)

            self.cod_venda = col1
            self.lb_mensagem_1.config(text="")

    def limpa_tela(self):
        self.lb_cod_venda_content.config(text="")
        self.nome_entry.delete(0, END)
        self.data_entry.delete(0, END)
        self.valor_entry.delete(0, END)
        self.busca_entry.delete(0, END)
        self.cod_venda = ""

        self.dataAtual = datetime.today().date()
        self.dataAtual = self.dataAtual.strftime('%d/%m/%Y')
        self.data_entry.insert(END, self.dataAtual)

    def add_venda(self):

        venda = Venda()

        venda.nome =  self.nome_entry.get()
        
        valor = "{:.02f}".format(float(self.valor_entry.get()))
        venda.valor = valor

        data = self.data_entry.get()
        data = data.replace('-', '/')
        venda.data = data

        data = datetime.strptime(data, '%d/%m/%Y').date()
        data_hoje = datetime.today().date()


        if (venda.nome == "" or venda.data == "" or venda.valor == ""):
            self.lb_mensagem_1.config(text="Prencha todos os campos")
        
        elif (data > data_hoje):
            self.lb_mensagem_1.config(text="Informe um data válida")    

        elif (self.cod_venda != ""):
            self.lb_mensagem_1.config(text="Não é possível adicionar com o mesmo código. Limpe a tela.")

        else:    
            mensagem = venda.add_venda()

            self.lb_mensagem_1.config(text=mensagem)

            self.select_lista()
            self.limpa_tela()

    def altera_venda(self):
        venda = Venda()
        
        
        venda.cod_venda = self.cod_venda
        venda.nome =  self.nome_entry.get()

        valor = self.valor_entry.get().replace(',', '.')
        valor = "{:.02f}".format(float(valor))
        venda.valor = valor

        data = self.data_entry.get()
        data = data.replace('-', '/')
        venda.data = data

        data = datetime.strptime(data, '%d/%m/%Y').date()
        data_hoje = datetime.today().date()
        
        if (venda.nome == "" or venda.data == "" or venda.valor == ""):
            self.lb_mensagem_1.config(text="Prencha todos os campos")

        elif (data > data_hoje):
            self.lb_mensagem_1.config(text="Informe um data válida")    

        else:    
            mensagem = venda.altera_venda()

            self.lb_mensagem_1.config(text=mensagem)

            self.select_lista()
            self.limpa_tela()

    def exclui_venda(self):
        venda = Venda()
        
        venda.cod_venda = self.cod_venda

        mensagem = venda.exclui_venda()
        self.lb_mensagem_1.config(text=mensagem)

        self.limpa_tela()
        self.select_lista()

    def busca_venda(self):
        self.listaVenda.delete(*self.listaVenda.get_children())

        venda = Venda()

        venda.nome = self.busca_entry.get()
        lista = venda.busca_vendas()
        
        if (lista == []):
            self.lb_mensagem_2.config(text="Nome não encontrado")

        else:
            self.lb_mensagem_2.config(text="")

        for row in lista:
            self.listaVenda.insert("", END, values=(row['cod_venda'], row['nome'], row['data'], row['valor']))

    def busca_venda_data(self):
        self.listaVenda.delete(*self.listaVenda.get_children())

        venda = Venda()

        venda.data_inicio = self.data_inicio_entry.get()
        venda.data_inicio = datetime.strptime(venda.data_inicio, '%d/%m/%Y').date()
        venda.data_fim = self.data_fim_entry.get()
        venda.data_fim = datetime.strptime(venda.data_fim, '%d/%m/%Y').date()

        if (venda.data_inicio > venda.data_fim):
            self.lb_mensagem_2.config(text="Coloque as datas de forma que a data incio esteja abaixo ou seja igual a data final.")
        
        else:
            self.lb_mensagem_2.config(text="")
            lista = venda.busca_venda_data()

            if (lista == []):
                self.lb_mensagem_2.config(text="Não foi realizada vendas nesse período.")

            for row in lista:
                self.listaVenda.insert("", END, values=(row['cod_venda'], row['nome'], row['data'], row['valor']))


    def busca_maior_venda(self):
        self.listaVenda.delete(*self.listaVenda.get_children())
        
        venda = Venda()
        lista = venda.busca_maior_venda()

        for row in lista:
            self.listaVenda.insert("", END, values=(row['cod_venda'], row['nome'], row['data'], row['valor']))


class Tela(Funcoes):
    def __init__(self):
        window = Tk()
        self.window = window
        self.tela()
        self.frames_da_tela()
        self.widgets_frame12()
        self.widgets_frame13()
        self.lista_frame2()
        self.select_lista()
        self.cod_venda = ""
        window.mainloop()

    def tela(self):
        self.window.title("Cadastro de Vendas")
        self.window.configure(background= '#1e3743')
        self.side, self.top = (self.window.winfo_screenwidth()), (self.window.winfo_screenheight())
        self.window.geometry('%dx%d+0+0' % (self.side,self.top))
        self.window.resizable(True, True)
        self.window.minsize(width=1000, height= 600)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('arial', 10, 'bold'))
        style.configure("Treeview", font=('arial', 10))

    def frames_da_tela(self):
        # Criação dos frames
        self.frame_1 = Frame(self.window, bd=4, bg='#dfe3ee', highlightthickness=3)
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)

        self.lb_frame_12 = LabelFrame(self.frame_1, text='Cadastro', bd=1, bg='#dfe3ee', fg='#107db2')
        self.lb_frame_12.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        
        self.lb_frame_13 = LabelFrame(self.frame_1, text='Busca', bd=1, bg='#dfe3ee', fg='#107db2')
        self.lb_frame_13.place(relx=0.02, rely=0.55, relwidth=0.96, relheight=0.4)

        self.frame_2 = Frame(self.window, bd=4, bg='#dfe3ee', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
        

    def widgets_frame12(self):
        # Criação do botao limpar
        self.bt_limpar = Button(self.lb_frame_12, text= "Limpar", bd=2, bg='#107db2', fg='white',
                                font=('arial', 10, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx= 0.544, rely=0.7, relwidth=0.1, relheight= 0.2)
       
        # Criação do botao alterar
        self.bt_alterar = Button(self.lb_frame_12, text="Alterar", bd=2, bg='#107db2', fg='white',
                                font=('arial', 10, 'bold'), command=self.altera_venda)
        self.bt_alterar.place(relx=0.646, rely=0.7, relwidth=0.1, relheight=0.2)
        
        # Criação do botao excluir
        self.bt_excluir = Button(self.lb_frame_12, text="Excluir", bd=2, bg='#107db2', fg='white',
                                font=('arial', 10, 'bold'), command=self.exclui_venda)
        self.bt_excluir.place(relx=0.748, rely=0.7, relwidth=0.1, relheight=0.2)
        
        # Criação do botao inserir
        self.bt_inserir = Button(self.lb_frame_12, text="Inserir", bd=2, bg='#107db2', fg='white',
                                font=('arial', 10, 'bold'), command=self.add_venda)
        self.bt_inserir.place(relx=0.85, rely=0.7, relwidth=0.1, relheight=0.2)


        # Criação da label e entrada do numero da venda
        self.lb_cod_venda = Label(self.lb_frame_12, text="N° venda", bg='#dfe3ee', fg='#107db2', font=('arial', 10))
        self.lb_cod_venda.place(relx=0.05, rely=0.1 )

        self.lb_cod_venda_content = Label(self.lb_frame_12, text='', bg='white', font=('arial', 10), anchor=W)
        self.lb_cod_venda_content.place(relx=0.05, rely=0.25, relwidth=0.1, relheight=0.2)
        
        # Criação da label e entrada do nome
        self.lb_nome = Label(self.lb_frame_12, text="Nome completo", bg='#dfe3ee', fg='#107db2', font=('arial', 10))
        self.lb_nome.place(relx=0.2, rely=0.1 )

        self.nome_entry = Entry(self.lb_frame_12, font=('arial', 10))
        self.nome_entry.place(relx=0.2, rely=0.25, relwidth=0.35, relheight=0.2)
       

        # Criação da label e entrada da data 
        self.lb_data = Label(self.frame_1, text="Data", bg='#dfe3ee', fg='#107db2', font=('arial', 10))
        self.lb_data.place(relx=0.6, rely=0.1)
        
        self.data_entry = DateEntry(self.lb_frame_12, width=12, background='#107db2', foreground='white', font=('arial', 10), 
            borderwidth=2, locale='pt_BR')
        self.data_entry.place(relx=0.6, rely=0.25, relwidth= 0.15, relheight=0.2)

        ## Criação da label e entrada do valor
        self.lb_valor = Label(self.lb_frame_12, text="Valor (R$ 0.00)", bg='#dfe3ee', fg='#107db2', font=('arial', 10))
        self.lb_valor.place(relx=0.8, rely=0.1)

        self.valor_entry = Entry(self.lb_frame_12, font=('arial', 10))
        self.valor_entry.place(relx=0.8, rely=0.25, relwidth=0.15, relheight=0.2)

        # Criação da label e entrada de mensagens
        self.lb_mensagem_1 = Label(self.lb_frame_12, text='', fg='#107db2', font=('arial', 10), anchor=W)
        self.lb_mensagem_1.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.2)
    
    def widgets_frame13(self):
        # Criação do botao buscar pelo nome
        self.bt_buscar_nome = Button(self.lb_frame_13, text="Buscar", bd=2, bg='#107db2', fg='white',
                                font=('arial', 10, 'bold'), command=self.busca_venda)
        self.bt_buscar_nome.place(relx= 0.26, rely=0.2, relwidth=0.1, relheight=0.25)

        # Criação do botao buscar pela data
        self.bt_buscar_data = Button(self.lb_frame_13, text="Buscar", bd=2, bg='#107db2', fg='white',
                                font=('arial', 10, 'bold'), command=self.busca_venda_data)
        self.bt_buscar_data.place(relx= 0.68, rely=0.2, relwidth=0.1, relheight=0.25)
       
        # Criação do botao buscar maior venda
        self.bt_buscar_venda_maior = Button(self.lb_frame_13, text="Maior venda", bd=2, bg='#107db2', fg='white',
                                font = ('arial', 10, 'bold'), command=self.busca_maior_venda)
        self.bt_buscar_venda_maior.place(relx=0.85, rely=0.2, relwidth=0.1, relheight=0.25)

        # Criação da label e entrada do nome
        self.lb_busca_venda = Label(self.lb_frame_13, text="Nome", bg='#dfe3ee', fg='#107db2', font=('arial', 10))
        self.lb_busca_venda.place(relx=0.05, rely=0.0 )

        self.busca_entry = Entry(self.lb_frame_13, font=('arial', 10))
        self.busca_entry.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.25)

        ## Criação da label e entrada da data do incio
        self.lb_data_inicio = Label(self.lb_frame_13, text="Data Inicio", bg='#dfe3ee', fg ='#107db2', font=('arial', 10))
        self.lb_data_inicio.place(relx= 0.45, rely= 0.0)
        
        self.data_inicio_entry = DateEntry(self.lb_frame_13, width=12, background='#107db2', foreground='white', 
            borderwidth=2, locale='pt_BR', font=('arial', 10))
        self.data_inicio_entry.place(relx= 0.45, rely= 0.2, relwidth= 0.1, relheight=0.25)
        
        ## Criação da label e entrada da data do fim
        self.lb_data_fim = Label(self.lb_frame_13, text="Data Fim", bg='#dfe3ee', fg='#107db2', font=('arial', 10))
        self.lb_data_fim.place(relx= 0.57, rely= 0.0)

        self.data_fim_entry = DateEntry(self.lb_frame_13, width=12, background='#107db2', foreground='white', 
            borderwidth=2, locale='pt_BR', font=('arial', 10))
        self.data_fim_entry.place(relx= 0.57, rely= 0.2, relwidth= 0.1, relheight=0.25)

        # Criação da label e entrada de mensagens
        self.lb_mensagem_2 = Label(self.lb_frame_13, text='', fg='#107db2', font=('arial', 10), anchor=W)
        self.lb_mensagem_2.place(relx=0.05, rely=0.6, relwidth=0.4, relheight=0.25)

       
    def lista_frame2(self):
        self.listaVenda = ttk.Treeview(self.frame_2, height=3,
            column=("col1", "col2", "col3", "col4", "col5"))

        self.listaVenda.heading("#0", text="")
        self.listaVenda.heading("#1", text="N° venda", anchor=W)
        self.listaVenda.heading("#2", text="Nome", anchor=W)
        self.listaVenda.heading("#3", text="Data", anchor=W)
        self.listaVenda.heading("#4", text="Valor", anchor=W)
        self.listaVenda.heading("#5", text="")
        self.listaVenda.column("#0", width=1)
        self.listaVenda.column("#1", width=30)
        self.listaVenda.column("#2", width=300)
        self.listaVenda.column("#3", width=60)
        self.listaVenda.column("#4", width=60)
        self.listaVenda.column("#5", width=1)
        self.listaVenda.place(relx=0.02, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaVenda.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=0.85)
        
        self.listaVenda.bind("<Double-1>", self.OnDoubleClick)

Tela()