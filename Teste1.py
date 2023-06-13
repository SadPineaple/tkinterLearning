from tkinter import *
from tkinter import ttk
import _sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image 
import webbrowser 
#from PIL import ImageTk, Image
import base64 

root = Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.foneRel = self.fone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 15)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 640, 'Telefone: ')
        self.c.drawString(50, 610, 'Cidade: ')

        self.c.setFont("Helvetica", 15)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.foneRel)
        self.c.drawString(150, 600, self.cidadeRel)

        self.c.rect(20,720, 550, 200, fill=False, stroke=True)


        self.c.showPage()
        self.c.save()
        self.printCliente()


class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = _sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando do banco de dados")
    def montaTabelas(self):
        self.conecta_bd();
        ### Criar tabela ###
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get()
    
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()
        
        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
        VALUES (?,?,?)""", (self.nome, self.fone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""
        SELECT  cod, 
                nome_cliente,
                telefone,
                cidade
            FROM clientes
            ORDER BY nome_cliente ASC;
        """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()

    def images_base64(self):
        self.btnovo_base64 = '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'

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4) 
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET 
                nome_cliente = ?,
                telefone = ?,
                cidade = ?
            WHERE cod = ?
        """, (self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.images_base64()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)
    def frames_da_tela(self):
        self.frame_1 = Frame(
            self.root, 
            bd = 4, 
            bg = '#dfe3ee', 
            highlightbackground= '#759fed', 
            highlightthickness=3
        )
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(
            self.root, 
            bd = 4, 
            bg = '#dfe3ee', 
            highlightbackground= '#759fed', 
            highlightthickness=3
        )
        self.frame_2.place(relx= 0.02, rely=0.5, relwidth= 0.96, relheight= 0.46)
    def widgets_frame1(self):
        self.canvas_bt = Canvas(
                                self.frame_1,
                                bd=0, bg='#1e3743',
                                highlightbackground = 'gray',
                                highlightthickness= 5
                                )
        self.canvas_bt.place(
                             relx=0.19,
                             rely= 0.08,
                             relwidth= 0.23,
                             relheight=0.19
                             )
        
        ### Criação do botão limpar
        self.bt_limpar = Button(
                                self.frame_1,
                                text= "Limpar",
                                bd=2,
                                bg = '#107bd2',
                                fg = '#fff',
                                activebackground="#108ecb",
                                activeforeground="#fff",
                                font= ('verdana', 8, 'bold'),
                                command= self.limpa_tela
                                ) 
        self.bt_limpar.place(
                             relx= 0.2,
                             rely= 0.1,
                             relwidth= 0.1,
                             relheight= 0.15
                             )
        
        ### Criação do botão buscar
        self.bt_buscar = Button(
                                self.frame_1,
                                text= "Buscar",
                                bd=2,
                                bg = '#107bd2',
                                fg = '#fff',
                                font= ('verdana', 8, 'bold'),
                                command = self.busca_cliente
                                )
        self.bt_buscar.place(
                             relx= 0.31,
                             rely= 0.1,
                             relwidth= 0.1,
                             relheight= 0.15
                             )
        
        ### Criação do botão novo
        ## imgNovo
        self.btnovo = PhotoImage(data=base64.b64decode(self.btnovo_base64))
        self.btnovo = self.btnovo.subsample(2, 2)

        self.bt_novo = Button(
                              self.frame_1,
                              image= self.btnovo,
                              command= self.add_cliente
                              )
        self.bt_novo.place(
                           relx= 0.6,
                           rely= 0.1,
                           width= 55,
                           height= 28  
                           )
        ### Criação do botão alterar
        self.bt_alterar = Button(
                                 self.frame_1,
                                 text= "Alterar",
                                 bd=2,
                                 bg = '#107bd2',
                                 fg = '#fff',
                                 font= ('verdana', 8, 'bold'),
                                 command= self.altera_cliente
                                 )
        self.bt_alterar.place(
                              relx= 0.71,
                              rely= 0.1,
                              relwidth= 0.1,
                              relheight= 0.15
                              )
        
        ### Criação do botão apagar
        self.bt_apagar = Button(
                                self.frame_1,
                                text= "Apagar",
                                bd=2,
                                bg = '#107bd2',
                                fg = '#fff',
                                font= ('verdana', 8, 'bold'),
                                command=self.deleta_cliente
                                )
        self.bt_apagar.place(
                             relx= 0.82,
                             rely= 0.1,
                             relwidth= 0.1,
                             relheight= 0.15
                             )

        ## Criaçao da label e entrada do código
        self.lb_codigo = Label(
                               self.frame_1,
                               text = "Código",
                               bg = '#dfe3ee',
                               fg='#107bd2'
                               )
        self.lb_codigo.place(
                             relx= 0.05,
                             rely= 0.06
                            )

        self.codigo_entry = Entry(
                                  self.frame_1
                                  )
        self.codigo_entry.place(
                                relx= 0.05,
                                rely= 0.16,
                                relwidth= 0.07
                                )

        ## Criaçao da label e entrada do nome
        self.lb_nome = Label(
                             self.frame_1,
                             text = "Nome",
                             bg = '#dfe3ee',
                             fg='#107bd2'
                             )
        self.lb_nome.place(
                           relx= 0.05,
                           rely= 0.36
                           )

        self.nome_entry = Entry(
                                self.frame_1
                                )
        self.nome_entry.place(
                              relx= 0.05,
                              rely= 0.46,
                              relwidth= 0.8
                              )

        ## Criaçao da label e entrada do telefone
        self.lb_fone = Label(
                             self.frame_1,
                             text = "Telefone",
                             bg = '#dfe3ee',
                             fg='#107bd2'
                             )
        self.lb_fone.place(
                           relx= 0.05,
                           rely= 0.6
                           )

        self.fone_entry = Entry(
                                self.frame_1
                                )
        self.fone_entry.place(
                              relx= 0.05,
                              rely= 0.7,
                              relwidth= 0.4
                              )

        ## Criaçao da label e entrada do cidade
        self.lb_cidade = Label(
                               self.frame_1,
                               text = "Cidade",
                               bg = '#dfe3ee',
                               fg='#107bd2'
                               )
        self.lb_cidade.place(
                             relx= 0.5,
                             rely= 0.6
                             )

        self.cidade_entry = Entry(
                                  self.frame_1
                                  )
        self.cidade_entry.place(
                                relx= 0.5,
                                rely= 0.7,
                                relwidth= 0.4
                                )
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height= 3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")
        
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx= 0.01, rely= 0.1, relwidth=0.95, relheight=0.85)
    
        self.scroolLista = Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label = "Relatório", menu= filemenu2)

        filemenu.add_command(label="Sair", command= Quit)
        filemenu.add_command(label="Limpa Cliente", command= self.limpa_tela)

        filemenu2.add_command(label="Ficha do cliente", command= self.geraRelatCliente)

Application()