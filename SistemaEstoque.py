from genericpath import exists
import customtkinter
from tkinter import CENTER, messagebox, ttk
from PIL import Image
import os
import sqlite3


file_path = os.path.dirname(os.path.realpath(__file__)) 
image = Image.open(file_path + "/lixeira.png")
image = image.resize((25,25))
image1 = customtkinter.CTkImage(image)


item_selecionado = None
idproduto = None
idproduto_saida = None

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')


def criar_bd(): #Cria o banco de dados
    conexao = sqlite3.connect("SistemaEstoque.db")
    cursor = conexao.cursor()

    cursor.execute("""
                                CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nomeP TEXT NOT NULL,
                                    quantidadeP INTEGER NOT NULL,
                                    precoP DECIMAL,
                                    descricaoP TEXT
                                    )
                                """)
    conexao.commit()
    cursor.close()
    

#=============================================================== Def's de cadastro ===============================================================#
def cancelar_cadastro(): #Vai ser usada em outra def
    messagebox.showerror("Mensagem Sistema", "Cadastro de produto cancelado pelo usuário.")
    cadastro_nome.delete(0, "end")
    cadastro_preco.delete(0, "end")
    entrada_desc.delete("1.0", "end")


def salvar_cadastro_produtos(): #Def pra cadastrar
        global nome_produto
        nome_produto = cadastro_nome.get().strip()  #Strip tira os espaços inúteis
        quantidade_produto = "0"
        preco_produto = cadastro_preco.get().strip()
        descricao_produto = entrada_desc.get('1.0', "end-1c").strip()

        if nome_produto and preco_produto and descricao_produto:

            conexao = sqlite3.connect('SistemaEstoque.db')
            cursor = conexao.cursor()
            conexao.commit()
            cursor.execute(f"INSERT INTO produtos (nomeP, quantidadeP, precoP, descricaoP) VALUES ('{nome_produto}', '{quantidade_produto}','{preco_produto}', "
                        f"'{descricao_produto}')")
            conexao.commit()
            conexao.close()

            cadastro_nome.delete(0, "end")
            cadastro_preco.delete(0, "end")
            entrada_desc.delete("1.0", "end")
            messagebox.showinfo("Mensagem Sistema", "Cadastro concluído!")

        elif nome_produto and preco_produto or preco_produto and descricao_produto or nome_produto and descricao_produto:
            messagebox.showerror("Mensagem do Sistema", "Erro! Algum campo está incompleto!")
        
        else:
            cancelar_cadastro()

        ler_dados()

#============================================================== Def's de edição ===============================================================#
def ler_dados():
    conexao = sqlite3.connect('SistemaEstoque.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    recebe_dados = cursor.fetchall()

    for i in tabela_estoque.get_children(): #######Não duplica os cadastro
        tabela_estoque.delete(i)

    for i in recebe_dados:  #Recebendo os dados dentro do cadastro, menos a qtd pq ainda nao utilizamos
        
        nomes = str(i[1])
        quantidade = str(i[2])
        preco = float(i[3])
        desc = str(i[4])
        tabela_estoque.insert("", "end", values=(nomes, quantidade, preco, desc))
    conexao.close()


def tabela_produtos_edicao():
    global idproduto
    conexao = sqlite3.connect("SistemaEstoque.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    recebe_dados = cursor.fetchall()
    
    for widget in scrollable_frame_edit.winfo_children():
        widget.destroy()    

    for i in recebe_dados:
        idproduto = int(i[0])  #Declarando pra usar depois
        nomes = str(i[1])
        itens = i [1]

        var_checkbox = customtkinter.BooleanVar(value=False)
        box_edit = customtkinter.CTkCheckBox(scrollable_frame_edit, text=itens, border_color="white", variable=var_checkbox, command=lambda n=nomes, v=var_checkbox: checkbox_event_edicao(n, v))
        box_edit.pack(pady=10, padx=10, fill="x")
    
    conexao.close()


def preencher_campos_edicao(nomes):  #Preencher os campos de edição com os dados do produto selecionado
    global produtoid
    conexao = sqlite3.connect("SistemaEstoque.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos where nomeP = ?", (nomes,))
    dados_produto = cursor.fetchone()

    if dados_produto:
        editar_nome.delete(0, "end")
        editar_nome.insert(0, dados_produto[1])

        editar_preco.delete(0, "end")
        editar_preco.insert(0, dados_produto[3])

        editar_desc.delete("1.0", "end")
        editar_desc.insert('1.0', dados_produto[4])
    conexao.close()


def checkbox_event_edicao(nomes, var_checkbox):
    global checkbox_anterior
    
    if var_checkbox.get() == 1:  # Se o checkbox foi marcado
        limpar_campos_edicao()
        if checkbox_anterior is not None and checkbox_anterior != var_checkbox: # Verifica se existe um checkbox previamente marcado e se o novo checkbox clicado é diferente do anterior.
            checkbox_anterior.set(0)  # Desmarca o checkbox anterior
        checkbox_anterior = var_checkbox  # Atualiza a referência
        preencher_campos_edicao(nomes)  # Carrega os dados do produto
    else:  # Se o checkbox foi desmarcado
        limpar_campos_edicao()
        checkbox_anterior = None  # Remove a referência ao checkbox anterior


def limpar_campos_edicao(): #Vai só limpar os campos de entry
    editar_nome.delete(0, 'end' )
    editar_preco.delete(0, "end")
    editar_desc.delete("1.0", "end")


def salvar_edicao(): #Salvar as edições feitas no produto
    global idproduto
    novo_nome_produto = editar_nome.get().strip()
    preco_produto = editar_preco.get().strip()
    descricao_produto = editar_desc.get('1.0', "end-1c").strip()
    preco_produto = int(editar_preco.get())

    if preco_produto > 0:
        conexao = sqlite3.connect("SistemaEstoque.db")
        cursor = conexao.cursor()

        cursor.execute(f"UPDATE produtos SET nomeP = '{novo_nome_produto}', precoP = '{preco_produto}', descricaoP = '{descricao_produto}' WHERE id = '{idproduto}'")
        conexao.commit()

        messagebox.showinfo("Mensagem Sistema", "Edição concluída!")

        tabela_produtos_edicao()
        ler_dados()

        editar_nome.delete(0, "end")
        editar_preco.delete(0, "end")
        editar_desc.delete("1.0", "end")
        idproduto = None
        conexao.close()
    else:
        messagebox.showerror("Mensagem Sistema", "Erro! Preço inválido!")


def excluir_produto(): ##Excluir o produto selecionado
    global nome_produto
    nome_produto = editar_nome.get().strip()
    if nome_produto:
        
        conexao = sqlite3.connect("SistemaEstoque.db")
        cursor = conexao.cursor()
        
        try:
            cursor.execute("DELETE FROM produtos WHERE nomeP = ?", (nome_produto,))
            conexao.commit()
            editar_nome.delete(0, "end")
            editar_preco.delete(0, "end")
            editar_desc.delete('1.0', 'end')
            messagebox.showinfo("Mensagem Sistema", "Produto excluído!")
            tabela_produtos_edicao()
            ler_dados()
            

        except sqlite3.Error as e:
            messagebox.showerror("Mensagem Sistema", "Erro ao excluir produto!")

        finally:
            conexao.close()
    

def cancelar_edicao(): ##Cancela edição do produto
    editar_nome.delete(0, "end")
    editar_preco.delete(0, "end")
    editar_desc.delete("1.0", "end")
    messagebox.showinfo("Mensagem Sistema", "Edição de produto cancelada!")
    tabela_produtos_edicao()
    ler_dados()


#============================================================== Def's de entrada ===============================================================#
def dados_entrada():
    conexao = sqlite3.connect("SistemaEstoque.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")

    recebe_dados = cursor.fetchall()

    for widget in scrollable_entrada.winfo_children():
        widget.destroy()

    for i in recebe_dados:
        nomes = str(i[1])
        itens = []
        itens.append(nomes)

        for i in itens:
            txt_entrada.configure(text=itens)
            box_entrada = customtkinter.CTkCheckBox(scrollable_entrada, text=itens, border_color="white", command=lambda n=nomes: preencher_campos_entrada(n))
            box_entrada.pack(pady=10, padx=10, fill="x")

    conexao.close()
    

def preencher_campos_entrada(nomes):
    conexao = sqlite3.connect("SistemaEstoque.db")
    cursor = conexao.cursor()
    
    cursor.execute(f"SELECT nomeP, quantidadeP FROM produtos WHERE nomeP = '{nomes}'")
    dados_produto = cursor.fetchone()  # Pegando apenas um registro
    
    conexao.close()

    if dados_produto:
        nome, quantidade = dados_produto
        
        # Se a quantidade for None, atribuímos uma string vazia
        quantidade = quantidade if quantidade is not None else ""

        entry_produto_entrada.delete(0, "end")
        entry_produto_entrada.insert(0, nome)
        entry_produto_entrada.configure(state="readonly")  

        quantidade_estoque_entrada.delete(0, "end")
        quantidade_estoque_entrada.insert(0, quantidade)
        quantidade_estoque_entrada.configure(state="readonly")  


def checkbox_event_entrada(nomes, var_checkbox):
    global checkbox_anterior, item_selecionado
    if var_checkbox.get() == True:
        if checkbox_anterior is not None and checkbox_anterior != var_checkbox:
            checkbox_anterior.set(0)
        preencher_campos_entrada(nomes)
        item_selecionado = nomes
        checkbox_anterior = var_checkbox
             
    else:
        if checkbox_anterior == var_checkbox:
            limpar_campos_edicao()
            item_selecionado = None
            checkbox_anterior = None



#============================================================== Def's de Saída ===============================================================#
def dados_saida():
    conexao = sqlite3.connect("SistemaEstoque.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")

    recebe_dados = cursor.fetchall()

    for widget in scrollable_saida.winfo_children():
        widget.destroy()

    for i in recebe_dados:
        nomes = str(i[1])
        itens = []
        itens.append(nomes)

        for i in itens:
            txt_saida.configure(text=itens)
            box_saida = customtkinter.CTkCheckBox(scrollable_saida, text=itens, border_color="white", command=lambda n=nomes: preencher_campos_saida(n))
            box_saida.pack(pady=10, padx=10, fill="x")

    conexao.close()


def preencher_campos_saida(nomes):
    conexao = sqlite3.connect("SistemaEstoque.db")
    cursor = conexao.cursor()
    
    cursor.execute(f"SELECT nomeP, quantidadeP FROM produtos WHERE nomeP = '{nomes}'")
    dados_produto = cursor.fetchone()  # Pegando apenas um registro
    
    conexao.close()

    if dados_produto:
        nome, quantidade = dados_produto  
        
        # Se a quantidade for None, atribuímos uma string vazia
        quantidade = quantidade if quantidade is not None else ""

        entry_produto_saida.delete(0, "end")
        entry_produto_saida.insert(0, nome)
        entry_produto_saida.configure(state="readonly")  

        quantidade_estoque_saida.delete(0, "end")
        quantidade_estoque_saida.insert(0, quantidade)
        quantidade_estoque_saida.configure(state="readonly")  


def checkbox_event_saida(nomes, var_checkbox): #Mesma coisa da edição, só que pra saída
    global checkbox_anterior, item_selecionado
    if var_checkbox.get() == True:
        if checkbox_anterior is not None and checkbox_anterior != var_checkbox:
            checkbox_anterior.set(0)
        preencher_campos_saida(nomes)
        item_selecionado = nomes
        checkbox_anterior = var_checkbox #seila
             
    else:
        if checkbox_anterior == var_checkbox:
            limpar_campos_edicao()
            item_selecionado = None
            checkbox_anterior = None


def cancelar_saida():
    entry_produto_saida.configure(state="normal")  
    entry_produto_saida.delete(0, "end")
    entry_produto_saida.configure(state="readonly")  

    quantidade_estoque_saida.configure(state="normal")  
    quantidade_estoque_saida.delete(0, "end")
    quantidade_estoque_saida.configure(state="readonly")  

    quantidade_retirada.delete(0, "end")  

    dados_saida()
    messagebox.showinfo("Mensagem Sistema", "Saída de produto cancelada!")
    



#============================================================== Frames / Telas ===============================================================#
def tela_cadastro():
    frame_editar.grid_forget()
    frame_saida.grid_forget()
    frame_relatorio.grid_forget()
    frame_entrada.grid_forget()
    tela.grid(row=0, column=1, padx=10, pady=10)
    tela.grid_propagate(False)
    botao_cadastrar.configure(state='disabled')
    botao_editar.configure(state='normal')
    botao_saida.configure(state='normal')
    botao_entrada.configure(state='normal')
    botao_relatorio.configure(state='normal')


def tela_editar():
    tela.grid_forget()
    frame_saida.grid_forget()
    frame_entrada.grid_forget()
    frame_relatorio.grid_forget()
    frame_editar.grid(row=0, column=1, padx=10, pady=10)
    frame_editar.grid_propagate(False)
    botao_cadastrar.configure(state='normal')
    botao_editar.configure(state='disabled')
    botao_saida.configure(state='normal')
    botao_entrada.configure(state='normal')
    botao_relatorio.configure(state='normal')
    tabela_produtos_edicao()

    
def tela_saida():
    tela.grid_forget()
    frame_editar.grid_forget()
    frame_relatorio.grid_forget()
    frame_entrada.grid_forget()
    frame_saida.grid(row=0, column=1, padx=10, pady=10)
    frame_saida.grid_propagate(False)
    botao_cadastrar.configure(state='normal')
    botao_editar.configure(state='normal')
    botao_saida.configure(state='disabled')
    botao_entrada.configure(state='normal')
    botao_relatorio.configure(state='normal')
    dados_saida()


def tela_entrada():
    tela.grid_forget()
    frame_editar.grid_forget()
    frame_saida.grid_forget()
    frame_relatorio.grid_forget()
    frame_entrada.grid(row=0, column=1, padx=10, pady=10)
    frame_entrada.grid_propagate(False)

    # Ux/Ui
    botao_cadastrar.configure(state='normal')
    botao_editar.configure(state='normal')
    botao_saida.configure(state='normal')
    botao_entrada.configure(state='disabled')
    botao_relatorio.configure(state='normal')
    dados_entrada()


def relatorio():
    # Frames que vão sumir
    tela.grid_forget()
    frame_editar.grid_forget()
    frame_entrada.grid_forget()
    frame_saida.grid_forget()
    frame_relatorio.grid(row=0, column=1)
    frame_relatorio.grid_propagate(False)
    ler_dados()

    #Botões
    botao_cadastrar.configure(state='normal')
    botao_editar.configure(state='normal')
    botao_saida.configure(state='normal')
    botao_entrada.configure(state='normal')
    botao_relatorio.configure(state='disabled')

    #Tela inicial relatório
    label_relatorio.configure(text="Relatório Estoque")
    tabela_estoque.grid(row=2, column=0, columnspan=5)
    columns_saida.grid_forget()
    columns_entrada.grid_forget()

    #Botões para alternar os relatórios
    botao_estoque.configure(state='disabled')
    botao_entrada.configure(state='normal')
    botao_saida_relatorio.configure(state='normal')


def saida_relatorio():
    label_relatorio.configure(text="Relatório Saída")
    tabela_estoque.grid_forget()
    columns_saida.grid_forget()
    columns_saida.grid(row=2, column=0, columnspan=5)
    columns_saida.grid_propagate(False)
    botao_estoque.configure(state='normal')
    botao_saida_relatorio.configure(state='disabled')
    botao_entrada.configure(state='normal')


def entrada_relatorio():
    label_relatorio.configure(text="Relatório Entrada")
    tabela_estoque.grid_forget()
    columns_saida.grid_forget()
    columns_entrada.grid(row=2, column=0, columnspan=5)
    columns_entrada.grid_propagate(False)
    botao_estoque.configure(state='normal')
    botao_saida_relatorio.configure(state='normal')
    botao_entrada.configure(state='disabled')


def exportar_relatorio():
    tela_export = customtkinter.CTkToplevel()
    tela_export.geometry('570x300')
    tela_export.title("Exportar Arquivos")
    tela_export.attributes("-topmost", True)
    tela_export.resizable(width=False, height=False)

    # Frame após clicar no botão de exportar
    frame_export = customtkinter.CTkFrame(tela_export, width=500, height=300)
    frame_export.pack(pady=10, anchor='center')
    frame_export.grid_propagate(False)

    # label da tela
    label_escolher_relatorio = customtkinter.CTkLabel(frame_export, text="Escolher Relatório(s)", font=("Arial", 20))
    label_escolher_relatorio.grid(row=0, column=0, pady=30)

    escolher_extensao = customtkinter.CTkLabel(frame_export, text="Escolher Extensão", font=("Arial", 20))
    escolher_extensao.grid(row=0, column=1, padx=50, pady=10)

    # CheckBox Tela Relatório
    exportar_estoque = customtkinter.CTkCheckBox(frame_export, text="Exportar Estoque", font=("Arial", 15),
                                                 corner_radius=15)
    exportar_estoque.grid(row=1, column=0, sticky="w", pady=10, padx=50)

    exportar_entrda = customtkinter.CTkCheckBox(frame_export, text="Exportar Entrada", font=("Arial", 15),
                                                corner_radius=15)
    exportar_entrda.grid(row=2, column=0, sticky="w", pady=10, padx=50)

    exportar_saida = customtkinter.CTkCheckBox(frame_export, text="Exportar Saída", font=("Arial", 15),
                                               corner_radius=15)
    exportar_saida.grid(row=3, column=0, sticky="w", pady=10, padx=50)

    # Extensões
    word = customtkinter.CTkCheckBox(frame_export, text="WORD", font=("Arial", 15), corner_radius=15)
    word.grid(row=1, column=1, sticky="w", pady=10, padx=50)

    pdf = customtkinter.CTkCheckBox(frame_export, text="PDF", font=("Arial", 15), corner_radius=15)
    pdf.grid(row=2, column=1, sticky="w", pady=10, padx=50)

    excel = customtkinter.CTkCheckBox(frame_export, text="EXCEL", font=("Arial", 15), corner_radius=15)
    excel.grid(row=3, column=1, sticky="w", padx=50, pady=10)

    salvar_export = customtkinter.CTkButton(frame_export, text="Cancelar", width=70, fg_color="red", command=sair)
    salvar_export.grid(row=4, column=0, pady=20, sticky="e")

    cancelar_export = customtkinter.CTkButton(frame_export, text="Salvar", width=70)
    cancelar_export.grid(row=4, column=1, sticky="w", padx=20)


def sair():
    janela.destroy()
    criar_bd.close()


if not os.path.exists("SistemaEstoque.db"):
    criar_bd()

janela = customtkinter.CTk()
janela.title("")
janela.geometry('820x420')

checkbox_anterior = customtkinter.BooleanVar()

# Trocar a cor da tabela
style = ttk.Style(master=janela)
style.theme_use('clam')
style.configure("Treeview", background="white", fieldbackground="#2D2D2D", foreground="black", rowheight=27,
                bordercolor="#83A2EB")

style.configure("Treeview.Heading", background="#83A2EB", bakcground="Black", relief="flat")
style.map("Treeview.Heading", background=[('active', '#a399f9')])



#==================================================================== Menu ==============================================================
menu = customtkinter.CTkFrame(master=janela, width=190, height=400, corner_radius=20)
menu.grid(row=0, column=0, padx=10, pady=10)
menu.pack_propagate(False)
# Resto da Tela
tela = customtkinter.CTkFrame(master=janela, width=590, height=400, corner_radius=20)
tela.grid(row=0, column=1, padx=10, pady=10)
tela.grid_propagate(False)


texto = customtkinter.CTkLabel(menu, text="Nome do\nSistema", font=("arial", 20, "bold")) # Label do menu
texto.pack(pady=40)

# Botões do menu
botao_cadastrar = customtkinter.CTkButton(master=menu, text='Cadastrar', command=tela_cadastro, corner_radius=5,
                                          text_color="black",
                                          fg_color="#4E92F4")
botao_cadastrar.pack(pady=5)

botao_editar = customtkinter.CTkButton(master=menu, text='Editar', command=tela_editar, corner_radius=5, text_color="black",
                                       fg_color="#4E92F4")
botao_editar.pack(pady=5)

botao_saida = customtkinter.CTkButton(master=menu, text='Saída', command=tela_saida, corner_radius=5,
                                      text_color="black",
                                      fg_color="#4E92F4")
botao_saida.pack(pady=5)

botao_entrada = customtkinter.CTkButton(master=menu, text='Entrada', command=tela_entrada, corner_radius=5,
                                        text_color="black",
                                        fg_color="#4E92F4")
botao_entrada.pack(pady=5)

botao_relatorio = customtkinter.CTkButton(master=menu, text='Relatório', command=relatorio, corner_radius=5,
                                          text_color="black",
                                          fg_color="#4E92F4")
botao_relatorio.pack(pady=5)

botao_encerrar_programa = customtkinter.CTkButton(menu, text="Sair", fg_color="red", command=sair, corner_radius=5,
                                                  text_color="white")
botao_encerrar_programa.pack(pady=30)



#==================================================================== Tela Cadastro ==============================================================
texto_inicial_cadastro = customtkinter.CTkLabel(tela, text="Cadastro do Produto", font=("arial", 20, "bold"))
texto_inicial_cadastro.grid(row=0, column=1, padx=10, pady=10)

texto_nome = customtkinter.CTkLabel(tela, text="Nome do produto:")
texto_nome.grid(row=1, column=0, padx=10, pady=10)

cadastro_nome = customtkinter.CTkEntry(tela, placeholder_text="Insira o nome do produto:", width=300)
cadastro_nome.grid(row=1, column=1, padx=10, pady=10)

texto_preco = customtkinter.CTkLabel(tela, text="Preço(R$):")
texto_preco.grid(row=2, column=0, padx=10, pady=10, sticky="e")

cadastro_preco = customtkinter.CTkEntry(tela, placeholder_text="0.00:", width=80)
cadastro_preco.grid(row=2, column=1, padx=10, pady=10, sticky="w")

cadastro_desc = customtkinter.CTkLabel(tela, text="Descrição:")
cadastro_desc.grid(row=3, column=0, padx=10, pady=10, sticky="e,n")

entrada_desc = customtkinter.CTkTextbox(master=tela, width=300, height=80)
entrada_desc.grid(row=3, column=1, padx=10, pady=10)

# Botão salvar e cancelar cadastro
botao_salvar_cadastro = customtkinter.CTkButton(master=tela, text='Salvar', corner_radius=5, text_color="black",
                                                fg_color="#4E92F4", command=salvar_cadastro_produtos)
botao_salvar_cadastro.grid(row=4, column=1, padx=10, pady=10, sticky="e")

botao_cancelar_cadastro = customtkinter.CTkButton(master=tela, text="Cancelar", corner_radius=5, text_color="white",
                                                  fg_color="red", command=cancelar_cadastro)
botao_cancelar_cadastro.grid(row=4, column=1, padx=10, pady=10, sticky="w")







#==================================================================== Tela Editar ==============================================================
frame_editar = customtkinter.CTkFrame(janela, width=590, height=400, corner_radius=20)
frame_editar.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
frame_editar.grid_propagate(False)

texto_inicial_editar = customtkinter.CTkLabel(frame_editar, text="Edição Produtos Cadastrados", font=("arial", 20, "bold"))
texto_inicial_editar.grid(row=0, column=0, padx=5, pady=5, columnspan=4, sticky="ew")

contador_produtos = customtkinter.CTkLabel(frame_editar, text=f"Produtos cadastrados: {1}", font=("arial", 14))
contador_produtos.grid(row=1, column=1, padx=1, pady=1, columnspan=2, sticky="ew")

buscar_entry_editar = customtkinter.CTkEntry(frame_editar, placeholder_text="Buscar Produto", width=230)
buscar_entry_editar.grid(row=1, column=0, rowspan=1, padx=5, pady=5, sticky="e")

editar_nome = customtkinter.CTkEntry(frame_editar, placeholder_text="Nome do produto", width=200)
editar_nome.grid(row=2, column=1, columnspan=2, padx=3, pady=3, sticky="w")

editar_preco = customtkinter.CTkEntry(frame_editar, placeholder_text="R$ 0.00", width=70)
editar_preco.grid(row=3, column=1, columnspan=2, padx=3, pady=3, sticky="w")

editar_desc = customtkinter.CTkTextbox(frame_editar, width=325, height=80)
editar_desc.grid(row=4, column=1, columnspan=3, padx=3, pady=3, sticky="w")

# Tabela de itens do frame de edição
scrollable_frame_edit = customtkinter.CTkScrollableFrame(frame_editar, border_width=2, border_color="white",
                                                    scrollbar_button_color="white")
scrollable_frame_edit.grid(row=2, column=0, rowspan=4, pady=10, padx=10)

txt_edit = customtkinter.CTkLabel(frame_editar)

# Botões do frame de edição
botao_excluir_editar = customtkinter.CTkButton(frame_editar, text="Excluir", fg_color="red", corner_radius=10,
                                                width=100, command=excluir_produto)
botao_excluir_editar.grid(row=5, column=1, columnspan=1, padx=5, pady=5, sticky="w")

botao_cancelar_editar = customtkinter.CTkButton(frame_editar, text="Cancelar", corner_radius=10, width=100,
                                                text_color="black", command=cancelar_edicao)
botao_cancelar_editar.grid(row=5, column=2, columnspan=1, padx=5, pady=5, sticky="w")

botao_salvar_editar = customtkinter.CTkButton(frame_editar, text="Salvar", corner_radius=10, width=100,
                                              text_color="black", command=salvar_edicao)

botao_salvar_editar.grid(row=5, column=3, columnspan=1, padx=5, pady=5, sticky="w")







#==================================================================== Saída ==============================================================
frame_saida = customtkinter.CTkFrame(janela, width=590, height=400, corner_radius=20)
frame_saida.grid(row=1, column=1)
frame_saida.grid_propagate(False)
label_inicial_saida = customtkinter.CTkLabel(frame_saida, text="Saída de Produto", font=("Arial", 20, "bold"))
label_inicial_saida.grid(row=0, column=0, padx=15, columnspan=2, sticky="en")

buscar_saida = customtkinter.CTkEntry(frame_saida, placeholder_text="Buscar Produto:", width=225)
buscar_saida.grid(row=1, column=0, rowspan=1, pady=25, padx=5)

# Tabela da saída
scrollable_saida = customtkinter.CTkScrollableFrame(frame_saida, border_width=2, border_color="white",
                                                    scrollbar_button_color="white")
scrollable_saida.grid(row=2, column=0, rowspan=4, pady=5, padx=25)

txt_saida = customtkinter.CTkLabel(master=frame_saida, text="")

entry_produto_saida = customtkinter.CTkEntry(frame_saida, placeholder_text=f"Produto: ", font=("Arial", 14), width=150)
entry_produto_saida.grid(row=1, column=1)

quantidade_estoque_saida = customtkinter.CTkEntry(frame_saida, placeholder_text="Quantidade:", width=90)
quantidade_estoque_saida.grid(row=1, column=2, sticky="w", padx=5)

quantidade_retirada = customtkinter.CTkEntry(frame_saida, placeholder_text="Quantidade:", width=90)
quantidade_retirada.grid(row=2, column=1, sticky="w", padx=5)

botao_adicionar = customtkinter.CTkButton(frame_saida, text="Adicionar item", width=60, fg_color="green")
botao_adicionar.grid(row=2, column=2, sticky="e", padx=5)

scrollable_saida2 = customtkinter.CTkScrollableFrame(frame_saida, border_width=2, border_color="white",
                                                     scrollbar_button_color="white", width=225)
scrollable_saida2.grid_columnconfigure(2, weight=1)
scrollable_saida2.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky="e")

botao_cancelar_saida = customtkinter.CTkButton(frame_saida, text="Cancelar", fg_color="red", width=80, command=cancelar_saida)
botao_cancelar_saida.grid(row=4, column=1, padx=5, sticky="w")

salvar_saida = customtkinter.CTkButton(frame_saida, text="Salvar", width=80)
salvar_saida.grid(row=4, column=2, padx=10, sticky="ne")






#==================================================================== Entrada ==============================================================
frame_entrada = customtkinter.CTkFrame(janela, width=590, height=400, corner_radius=20)
frame_entrada.grid(row=1, column=1)
frame_entrada.grid_propagate(False)
text_entrada = customtkinter.CTkLabel(frame_entrada, text="Entrada de Produto", font=("Arial", 20, "bold"))
text_entrada.grid(row=0, column=0, padx=15, columnspan=2, sticky="en")

buscar_entrada = customtkinter.CTkEntry(frame_entrada, placeholder_text="Buscar Produto:", width=225)
buscar_entrada.grid(row=1, column=0, rowspan=1, pady=25, padx=5)

# Tabela 1 do frame de Entrada
scrollable_entrada = customtkinter.CTkScrollableFrame(frame_entrada, border_width=2, border_color="white",
                                                      scrollbar_button_color="white")
scrollable_entrada.grid(row=2, column=0, rowspan=4, pady=5, padx=25)

txt_entrada = customtkinter.CTkLabel(master=frame_entrada, text="")

entry_produto_entrada = customtkinter.CTkEntry(frame_entrada, placeholder_text=f"Produto: ", font=("Arial", 14),
                                                   width=150)
entry_produto_entrada.grid(row=1, column=1)

quantidade_estoque_entrada = customtkinter.CTkEntry(frame_entrada, placeholder_text="Quantidade:", width=90)
quantidade_estoque_entrada.grid(row=1, column=2, sticky="w", padx=5)

quantidade_entrada = customtkinter.CTkEntry(frame_entrada, placeholder_text="Quantidade:", width=90)
quantidade_entrada.grid(row=2, column=1, sticky="w", padx=5)

botao_adicionar_entrada = customtkinter.CTkButton(frame_entrada, text="Adicionar item", width=60, fg_color="green")
botao_adicionar_entrada.grid(row=2, column=2, sticky="e", padx=5)

tabela_dois_entrada = ["Produto 1", "Produto 2", "Produto 3", "Produto 4", "Produto 5", "Produto 6", "Produto 7",
                       "Produto 8"]
scrollable_entrada2 = customtkinter.CTkScrollableFrame(frame_entrada, border_width=2, border_color="white",
                                                       scrollbar_button_color="white", width=225)
scrollable_entrada2.grid_columnconfigure(2, weight=1)
scrollable_entrada2.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky="e")

cancelar_entrada = customtkinter.CTkButton(frame_entrada, text="Cancelar", fg_color="red", width=80)
cancelar_entrada.grid(row=4, column=1, padx=5, sticky="w")

salvar_entrada = customtkinter.CTkButton(frame_entrada, text="Salvar", width=80)
salvar_entrada.grid(row=4, column=2, padx=10, sticky="ne")






#=============================================================== Frame e label relatório =====================================================
frame_relatorio = customtkinter.CTkFrame(janela, width=590, height=400, corner_radius=20)
frame_relatorio.grid(row=1, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")
frame_relatorio.grid_propagate(False)
frame_relatorio.grid_columnconfigure(0, weight=1)
frame_relatorio.grid_rowconfigure(2, weight=1)

label_relatorio = customtkinter.CTkLabel(frame_relatorio, text="Relatório Estoque", font=("Arial", 20, "bold"))
label_relatorio.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

# Campo de busca
buscar_relatorio = customtkinter.CTkEntry(frame_relatorio, placeholder_text="Buscar Produto", width=200)
buscar_relatorio.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Botão de exportar
botao_exportar = customtkinter.CTkButton(frame_relatorio, text="Exportar", fg_color="green", width=80,
                                         command=exportar_relatorio)
botao_exportar.grid(row=1, column=1, pady=5, padx=5, sticky='w')

tamanho_coluna = 120
altura_treeview = 30

# Tabela Estoque
colunas_estoque = ["Produto", "Quantidade", "Preço (R$)", "Descrição"]
tabela_estoque = ttk.Treeview(frame_relatorio, columns=colunas_estoque, show="headings", height=altura_treeview)
tabela_estoque.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

for coluna_estoque in colunas_estoque:
    tabela_estoque.heading(coluna_estoque, text=coluna_estoque)
    tabela_estoque.column(coluna_estoque, width=tamanho_coluna + 22, anchor=CENTER)

# Tabela Entrada
colunas_entrada = ["Produto", "Quantidade", "Data / Hora"]
columns_entrada = ttk.Treeview(frame_relatorio, columns=colunas_entrada, show="headings", height=altura_treeview)
columns_entrada.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

for coluna in colunas_entrada:
    columns_entrada.heading(coluna, text=coluna)
    columns_entrada.column(coluna, width=tamanho_coluna + 70)

# Tabela Saída
colunas_saida = ["Produto", "Quantidade", "Data / Hora"]
columns_saida = ttk.Treeview(frame_relatorio, columns=colunas_saida, show="headings", height=altura_treeview)
columns_saida.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

for coluna in colunas_saida:
    columns_saida.heading(coluna, text=coluna)
    columns_saida.column(coluna, width=tamanho_coluna + 70)

# Botões do estoque
frame_botoes = customtkinter.CTkFrame(frame_relatorio, fg_color="transparent")
frame_botoes.grid(row=5, column=0, columnspan=3, pady=10, sticky="n")

botao_estoque = customtkinter.CTkButton(frame_botoes, text="Estoque", width=80, command=relatorio)
botao_estoque.grid(row=0, column=0, padx=2)

botao_entrada = customtkinter.CTkButton(frame_botoes, text="Entrada", width=80, command=entrada_relatorio)
botao_entrada.grid(row=0, column=1, padx=2)

botao_saida_relatorio = customtkinter.CTkButton(frame_botoes, text="Saída", width=80, command=saida_relatorio)
botao_saida_relatorio.grid(row=0, column=2, padx=2)

janela.mainloop()
