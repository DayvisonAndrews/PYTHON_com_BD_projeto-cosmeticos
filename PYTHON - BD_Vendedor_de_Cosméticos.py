import psycopg2
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import datetime


resultados = 0
Pesq_cliente = "ASC"
Pesq_produto = "ASC"
Pesq_pedido = "ASC"



# Função de conexão ao banco de dados
def Conexao_BD(query, dados=None):
    global resultados

    try:
        # Conexão com o banco de dados PostgreSQL
        conexao = psycopg2.connect(
            host="localhost",
            database="Vendedores_de_Cosmeticos",
            user="admin",
            password="a123"
        )
        cursor = conexao.cursor()
        print("Conexão ao banco de dados Aberta.")

        # Executa a consulta
        if dados == None:
            cursor.execute(query)
        else:
            cursor.execute(query, (dados))

        resultados = cursor.fetchall()

        if resultados:
            return resultados
        else:
            messagebox.showinfo("Resultado", "Nenhum resultado encontrado.")
            return []

    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {error}")

    finally:
        if conexao:
            cursor.close()
            conexao.close()
            print("Conexão ao banco de dados Fechada.")






# Funções para abrir novas janelas
def abrir_clientes():
    janela_clientes = Toplevel(janela)
    janela_clientes.title("Clientes")
    Label(janela_clientes, text="->>> Aqui você pode cadastrar e pesquisar clientes <<<- \n").pack()

    def abrir_CADclientes():
        janela_cad_clientes = Toplevel()
        janela_cad_clientes.title("Cadastro de Clientes")
        Label(janela_cad_clientes, text="->>> Tela para cadastrar novos Clientes <<<- \n").grid(row=0, column=0, columnspan=4)

        # Lista para armazenar os Clientes cadastrados
        clientes_cadastrados = []

        # Função para obter o próximo código de cliente automaticamente
        def obter_proximo_codigo():
            conexao = psycopg2.connect(
                host="localhost",
                database="Vendedores_de_Cosmeticos",
                user="admin",
                password="a123"
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT MAX(id_cliente) FROM public.clientes")
            resultado = cursor.fetchone()[0]
            cursor.close()
            conexao.close()

            TOTAL_clientes_cadastrados = len(clientes_cadastrados)

            if resultado:
                return str(int(resultado) + 1 + TOTAL_clientes_cadastrados)  # Incrementa o maior código em 1
            else:
                return "1"  # Se não houver clientes cadastrados, começa do código 1

        # Função para adicionar o cliente à lista ou substituí-lo
        def adicionar_cliente():
            id_cliente = entrada_cod_cliente.get()
            nome_cliente = entrada_nome_cliente.get()
            cpf_cliente = entrada_cpf_cliente.get()
            entrada_telefone_cliente.get()
            entrada_email_cliente.get()
            entrada_cep_cliente.get()
            entrada_rua_cliente.get()
            entrada_numero_cliente.get()
            entrada_complemento_cliente.get()
            entrada_ponto_referencia_cliente.get()
            entrada_bairro_cliente.get()
            entrada_cidade_cliente.get()
            entrada_estado_cliente.get()
            entrada_pais_cliente.get()

            if id_cliente and nome_cliente and cpf_cliente:
                try:
                    cliente_existe = False

                    # Verificar se o código do cliente já existe na lista
                    for i, cliente in enumerate(clientes_cadastrados):
                        if cliente[0] == id_cliente:
                            clientes_cadastrados[i] = (id_cliente, nome_cliente, cpf_cliente, entrada_telefone_cliente.get(), entrada_email_cliente.get(), entrada_cep_cliente.get(), entrada_rua_cliente.get(), entrada_numero_cliente.get(), entrada_complemento_cliente.get(), entrada_ponto_referencia_cliente.get(), entrada_bairro_cliente.get(), entrada_cidade_cliente.get(), entrada_estado_cliente.get(), entrada_pais_cliente.get())
                            cliente_existe = True
                            messagebox.showinfo("Cliente Substituído", f"Cliente {nome_cliente} substituído com sucesso!")
                            break

                    if not cliente_existe:
                        clientes_cadastrados.append((id_cliente, nome_cliente, cpf_cliente, entrada_telefone_cliente.get(), entrada_email_cliente.get(), entrada_cep_cliente.get(), entrada_rua_cliente.get(), entrada_numero_cliente.get(), entrada_complemento_cliente.get(), entrada_ponto_referencia_cliente.get(), entrada_bairro_cliente.get(), entrada_cidade_cliente.get(), entrada_estado_cliente.get(), entrada_pais_cliente.get()))
                        messagebox.showinfo("Cliente Adicionado", f"Cliente {nome_cliente} adicionado com sucesso!")

                    # Atualizar a exibição dos clientes adicionados
                    atualizar_lista_clientes()

                    # Limpar campos após adicionar
                    entrada_nome_cliente.delete(0, END)
                    entrada_cpf_cliente.delete(0, END)
                    entrada_telefone_cliente.delete(0, END)
                    entrada_email_cliente.delete(0, END)
                    entrada_cep_cliente.delete(0, END)
                    entrada_rua_cliente.delete(0, END)
                    entrada_numero_cliente.delete(0, END)
                    entrada_complemento_cliente.delete(0, END)
                    entrada_ponto_referencia_cliente.delete(0, END)
                    entrada_bairro_cliente.delete(0, END)
                    entrada_cidade_cliente.delete(0, END)
                    entrada_estado_cliente.delete(0, END)
                    entrada_pais_cliente.delete(0, END)

                    # Preencher o próximo código automaticamente
                    entrada_cod_cliente.delete(0, END)
                    entrada_cod_cliente.insert(0, obter_proximo_codigo())


                except Exception as e:
                    messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        # Função para atualizar a lista de clientes na interface
        def atualizar_lista_clientes():
            lista_clientes.delete(0, END)  # Limpar lista
            for cliente in clientes_cadastrados:
                lista_clientes.insert(END, f"ID: {cliente[0]} - Nome: {cliente[1]} - CPF: {cliente[2]} - Telefone: {cliente[3]} - Email: {cliente[4]} - CEP: {cliente[5]} - Rua: {cliente[6]} - Número: {cliente[7]} - Complemento: {cliente[8]} - Ponto de Referência: {cliente[9]} - Bairro: {cliente[10]} - Cidade: {cliente[11]} - Estado: {cliente[12]} - País: {cliente[13]}")

        # Função para enviar os clientes ao banco de dados (com atualização se o código já existir)
        def enviar_ao_banco():
            if clientes_cadastrados:
                conexao = psycopg2.connect(
                    host="localhost",
                    database="Vendedores_de_Cosmeticos",
                    user="admin",
                    password="a123"
                )
                cursor = conexao.cursor()

                for cliente in clientes_cadastrados:
                    id_cliente, nome_cliente, cpf, telefone, email, endereco_cep, endereco_rua, endereco_numero, endereco_complemento, endereco_pontoreferencia, endereco_bairro, endereco_cidade, endereco_estado, endereco_pais = cliente

                    # Verificar se o cliente já existe no banco
                    cursor.execute("SELECT id_cliente FROM public.clientes WHERE id_cliente = %s", (id_cliente,))
                    resultado = cursor.fetchone()

                    if resultado:
                        # Se o cliente já existe, atualizá-lo
                        query_update = """
                                UPDATE public.clientes
                                SET nome_cliente = %s, cpf = %s, telefone = %s, email = %s, endereco_cep = %s, endereco_rua = %s, endereco_numero = %s, endereco_complemento = %s, endereco_pontoreferencia = %s, endereco_bairro = %s, endereco_cidade = %s, endereco_estado = %s, endereco_pais = %s
                                WHERE id_cliente = %s
                                """
                        cursor.execute(query_update, (nome_cliente, cpf, telefone, email, endereco_cep, endereco_rua, endereco_numero, endereco_complemento, endereco_pontoreferencia, endereco_bairro, endereco_cidade, endereco_estado, endereco_pais))
                        messagebox.showinfo("Cliente Atualizado",
                                            f"Cliente {nome_cliente} atualizado no banco de dados.")
                    else:
                        # Se não existir, inseri-lo
                        query_insert = """
                                INSERT INTO public.clientes (id_cliente, nome_cliente, cpf, telefone, email, endereco_cep, endereco_rua, endereco_numero, endereco_complemento, endereco_pontoreferencia, endereco_bairro, endereco_cidade, endereco_estado, endereco_pais)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                        cursor.execute(query_insert, (id_cliente, nome_cliente, cpf, telefone, email, endereco_cep, endereco_rua, endereco_numero, endereco_complemento, endereco_pontoreferencia, endereco_bairro, endereco_cidade, endereco_estado, endereco_pais))

                conexao.commit()
                cursor.close()
                conexao.close()

                messagebox.showinfo("Sucesso", "Todos os clientes foram processados no banco de dados.")
                clientes_cadastrados.clear()
                atualizar_lista_clientes()
            else:
                messagebox.showinfo("Atenção", "Nenhum cliente cadastrado para enviar.")

        # Layout em duas colunas para os campos de entrada
        Label(janela_cad_clientes, text="ID do Cliente:").grid(row=1, column=0, sticky=W)
        entrada_cod_cliente = Entry(janela_cad_clientes)
        entrada_cod_cliente.grid(row=1, column=1)

        # Preencher o campo de código do cliente automaticamente ao abrir a janela
        entrada_cod_cliente.insert(0, obter_proximo_codigo())

        Label(janela_cad_clientes, text="Nome do Cliente:").grid(row=2, column=0, sticky=W)
        entrada_nome_cliente = Entry(janela_cad_clientes)
        entrada_nome_cliente.grid(row=2, column=1)

        Label(janela_cad_clientes, text="CPF:").grid(row=3, column=0, sticky=W)
        entrada_cpf_cliente = Entry(janela_cad_clientes)
        entrada_cpf_cliente.grid(row=3, column=1)

        Label(janela_cad_clientes, text="Telefone:").grid(row=4, column=0, sticky=W)
        entrada_telefone_cliente = Entry(janela_cad_clientes)
        entrada_telefone_cliente.grid(row=4, column=1)

        Label(janela_cad_clientes, text="Email:").grid(row=5, column=0, sticky=W)
        entrada_email_cliente = Entry(janela_cad_clientes)
        entrada_email_cliente.grid(row=5, column=1)

        Label(janela_cad_clientes, text="CEP:").grid(row=6, column=0, sticky=W)
        entrada_cep_cliente = Entry(janela_cad_clientes)
        entrada_cep_cliente.grid(row=6, column=1)

        Label(janela_cad_clientes, text="Rua:").grid(row=7, column=0, sticky=W)
        entrada_rua_cliente = Entry(janela_cad_clientes)
        entrada_rua_cliente.grid(row=7, column=1)

        Label(janela_cad_clientes, text="Número:").grid(row=8, column=0, sticky=W)
        entrada_numero_cliente = Entry(janela_cad_clientes)
        entrada_numero_cliente.grid(row=8, column=1)

        Label(janela_cad_clientes, text="Complemento:").grid(row=9, column=0, sticky=W)
        entrada_complemento_cliente = Entry(janela_cad_clientes)
        entrada_complemento_cliente.grid(row=9, column=1)

        Label(janela_cad_clientes, text="Ponto de Referência:").grid(row=10, column=0, sticky=W)
        entrada_ponto_referencia_cliente = Entry(janela_cad_clientes)
        entrada_ponto_referencia_cliente.grid(row=10, column=1)

        Label(janela_cad_clientes, text="Bairro:").grid(row=1, column=2, sticky=W)
        entrada_bairro_cliente = Entry(janela_cad_clientes)
        entrada_bairro_cliente.grid(row=1, column=3)

        Label(janela_cad_clientes, text="Cidade:").grid(row=2, column=2, sticky=W)
        entrada_cidade_cliente = Entry(janela_cad_clientes)
        entrada_cidade_cliente.grid(row=2, column=3)

        Label(janela_cad_clientes, text="Estado:").grid(row=3, column=2, sticky=W)
        entrada_estado_cliente = Entry(janela_cad_clientes)
        entrada_estado_cliente.grid(row=3, column=3)

        Label(janela_cad_clientes, text="País:").grid(row=4, column=2, sticky=W)
        entrada_pais_cliente = Entry(janela_cad_clientes)
        entrada_pais_cliente.grid(row=4, column=3)

        botao_adicionar = Button(janela_cad_clientes, text="Adicionar Cliente", command=adicionar_cliente)
        botao_adicionar.grid(row=11, column=0, columnspan=2, pady=10)

        # Listbox para mostrar a lista de clientes adicionados
        Label(janela_cad_clientes, text="Clientes Adicionados:").grid(row=12, column=0, columnspan=2, sticky=W)
        lista_clientes = Listbox(janela_cad_clientes, height=10, width=50)
        lista_clientes.grid(row=13, column=0, columnspan=2)

        botao_enviar = Button(janela_cad_clientes, text="Enviar ao Banco", command=enviar_ao_banco)
        botao_enviar.grid(row=14, column=0, columnspan=2, pady=10)





    def pesquisar_cliente():
        global Pesq_cliente
        cod_cliente = entrada_cliente.get()
        if cod_cliente.isdigit():
            query = """
                            SELECT id_cliente, nome_cliente, cpf, telefone, email, endereco_cep, endereco_rua, endereco_numero, endereco_complemento, endereco_pontoreferencia, endereco_bairro, endereco_cidade, endereco_estado, endereco_pais
                            FROM public.clientes
                            WHERE id_cliente = %s;
                            """
            resultados = Conexao_BD(query, (cod_cliente,))
        else:
            if (Pesq_cliente == "ASC"):
                query = """
                                SELECT * FROM public.clientes
                                ORDER BY id_cliente ASC;
                                """
                resultados = Conexao_BD(query)
                Pesq_cliente = "DESC"
            else:
                query = """
                                SELECT * FROM public.clientes
                                ORDER BY id_cliente DESC;
                                """
                resultados = Conexao_BD(query)
                Pesq_cliente = "ASC"

        if resultados:
            texto_resultado.delete(1.0, END)
            for row in resultados:
                texto_resultado.insert(END, f"ID Cliente: {row[0]}, Nome: {row[1]}, CPF: {row[2]}, Telefone: {row[3]}, E-mail: {row[4]}, \nENDEREÇO >> CEP: {row[5]}, Rua: {row[6]}, Número: {row[7]}, Complemento: {row[8]}, Ponto de Referência: {row[9]}, Bairro: {row[10]}, Cidade: {row[11]}, Estado: {row[12]}, País: {row[13]} \n\n")
        else:
            messagebox.showinfo("Resultado", "Nenhum cliente encontrado.")



    # Botão de cadastro de cliente
    botao_CADclientes = Button(janela_clientes, text="+ Cadastrar Cliente +", command=abrir_CADclientes)
    botao_CADclientes.pack(pady=10)

    # Espaço entre botões
    Label(janela_clientes, text="\n").pack()

    label_pedido = Label(janela_clientes, text="Digite o código do Cliente:")
    label_pedido.pack()

    entrada_cliente = Entry(janela_clientes)
    entrada_cliente.pack()

    # Botão de pesquisa de cliente
    botao_pesquisar = Button(janela_clientes, text="Pesquisar", command=pesquisar_cliente)
    botao_pesquisar.pack()

    # Área de texto para mostrar o resultado da consulta
    texto_resultado = Text(janela_clientes, height=10, width=80)
    texto_resultado.pack()






def abrir_produtos():
    janela_produtos = Toplevel(janela)
    janela_produtos.title("Produtos")
    Label(janela_produtos, text="->>> Aqui você pode cadastrar e pesquisar produtos <<<- \n").pack()

    def abrir_CADprodutos():
        janela_cad_produtos = Toplevel()
        janela_cad_produtos.title("Cadastro de Produtos")
        Label(janela_cad_produtos, text="->>> Tela para cadastrar novos produtos <<<- \n").pack()

        # Lista para armazenar os produtos cadastrados
        produtos_cadastrados = []

        # Função para obter o próximo código de produto automaticamente
        def obter_proximo_codigo():
            conexao = psycopg2.connect(
                host="localhost",
                database="Vendedores_de_Cosmeticos",
                user="admin",
                password="a123"
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT MAX(cod_produto) FROM public.produtos")
            resultado = cursor.fetchone()[0]
            cursor.close()
            conexao.close()

            TOTAL_produtos_cadastrados = len(produtos_cadastrados)

            if resultado:
                return str(int(resultado) + 1 + TOTAL_produtos_cadastrados)  # Incrementa o maior código em 1
            else:
                return "1"  # Se não houver produtos cadastrados, começa do código 1

        # Função para adicionar o produto à lista ou substituí-lo
        def adicionar_produto():
            cod_produto = entrada_cod_produto.get()
            nome_produto = entrada_nome_produto.get()
            valor_produto = entrada_valor_produto.get()

            if cod_produto and nome_produto and valor_produto:
                try:
                    valor_produto = float(valor_produto)  # Converter o valor para número
                    produto_existe = False

                    # Verificar se o código do produto já existe na lista
                    for i, produto in enumerate(produtos_cadastrados):
                        if produto[0] == cod_produto:
                            produtos_cadastrados[i] = (cod_produto, nome_produto, valor_produto)
                            produto_existe = True
                            messagebox.showinfo("Produto Substituído",
                                                f"Produto {nome_produto} substituído com sucesso!")
                            break

                    if not produto_existe:
                        produtos_cadastrados.append((cod_produto, nome_produto, valor_produto))
                        messagebox.showinfo("Produto Adicionado", f"Produto {nome_produto} adicionado com sucesso!")

                    # Atualizar a exibição dos produtos adicionados
                    atualizar_lista_produtos()

                    # Limpar campos após adicionar
                    entrada_nome_produto.delete(0, END)
                    entrada_valor_produto.delete(0, END)

                    # Preencher o próximo código automaticamente
                    entrada_cod_produto.delete(0, END)
                    entrada_cod_produto.insert(0, obter_proximo_codigo())

                except ValueError:
                    messagebox.showerror("Erro", "Valor do produto deve ser numérico.")
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        # Função para atualizar a lista de produtos na interface
        def atualizar_lista_produtos():
            lista_produtos.delete(0, END)  # Limpar lista
            for produto in produtos_cadastrados:
                lista_produtos.insert(END, f"Código: {produto[0]} - Nome: {produto[1]} - Valor: R$ {produto[2]:.2f}")

        # Função para enviar os produtos ao banco de dados (com atualização se o código já existir)
        def enviar_ao_banco():
            if produtos_cadastrados:
                conexao = psycopg2.connect(
                    host="localhost",
                    database="Vendedores_de_Cosmeticos",
                    user="admin",
                    password="a123"
                )
                cursor = conexao.cursor()

                for produto in produtos_cadastrados:
                    cod_produto, nome_produto, valor_produto = produto

                    # Verificar se o produto já existe no banco
                    cursor.execute("SELECT cod_produto FROM public.produtos WHERE cod_produto = %s", (cod_produto,))
                    resultado = cursor.fetchone()

                    if resultado:
                        # Se o produto já existe, atualizá-lo
                        query_update = """
                        UPDATE public.produtos
                        SET nome_produto = %s, valor = %s
                        WHERE cod_produto = %s
                        """
                        cursor.execute(query_update, (nome_produto, valor_produto, cod_produto))
                        messagebox.showinfo("Produto Atualizado",
                                            f"Produto {nome_produto} atualizado no banco de dados.")
                    else:
                        # Se não existir, inseri-lo
                        query_insert = """
                        INSERT INTO public.produtos (cod_produto, nome_produto, valor)
                        VALUES (%s, %s, %s)
                        """
                        cursor.execute(query_insert, (cod_produto, nome_produto, valor_produto))

                conexao.commit()
                cursor.close()
                conexao.close()

                messagebox.showinfo("Sucesso", "Todos os produtos foram processados no banco de dados.")
                produtos_cadastrados.clear()
                atualizar_lista_produtos()
            else:
                messagebox.showinfo("Atenção", "Nenhum produto cadastrado para enviar.")

        # Layout da interface de cadastro de produtos
        Label(janela_cad_produtos, text="Código do Produto:").pack()
        entrada_cod_produto = Entry(janela_cad_produtos)
        entrada_cod_produto.pack()

        # Preencher o campo de código do produto automaticamente ao abrir a janela
        entrada_cod_produto.insert(0, obter_proximo_codigo())

        Label(janela_cad_produtos, text="Nome do Produto:").pack()
        entrada_nome_produto = Entry(janela_cad_produtos)
        entrada_nome_produto.pack()

        Label(janela_cad_produtos, text="Valor do Produto:").pack()
        entrada_valor_produto = Entry(janela_cad_produtos)
        entrada_valor_produto.pack()

        botao_adicionar = Button(janela_cad_produtos, text="Adicionar Produto", command=adicionar_produto)
        botao_adicionar.pack(pady=10)

        # Listbox para mostrar a lista de produtos adicionados
        Label(janela_cad_produtos, text="Produtos Adicionados:").pack()
        lista_produtos = Listbox(janela_cad_produtos, height=10, width=50)
        lista_produtos.pack()

        botao_enviar = Button(janela_cad_produtos, text="Enviar ao Banco", command=enviar_ao_banco)
        botao_enviar.pack(pady=10)


    def pesquisar_produto():
        global Pesq_produto
        cod_produto = entrada_produto.get()
        if cod_produto.isdigit():
            query = """
                    SELECT cod_produto, nome_produto, valor
                    FROM public.produtos
                    WHERE cod_produto = %s;
                    """
            resultados = Conexao_BD(query, (cod_produto,))
        else:
            if(Pesq_produto == "ASC"):
                query = """
                        SELECT * FROM public.produtos
                        ORDER BY cod_produto ASC;
                        """
                resultados = Conexao_BD(query)
                Pesq_produto = "DESC"
            else:
                query = """
                        SELECT * FROM public.produtos
                        ORDER BY cod_produto DESC;
                        """
                resultados = Conexao_BD(query)
                Pesq_produto = "ASC"


        if resultados:
            texto_resultado.delete(1.0, END)
            for row in resultados:
                texto_resultado.insert(END, f"Nº Produto: {row[0]}, Nome: {row[1]}, Valor: {row[2]}, \n")
        else:
            messagebox.showinfo("Resultado", "Nenhum produto encontrado.")

    # Botão de cadastro de produto
    botao_CADprodutos = Button(janela_produtos, text="+ Cadastrar Produto +", command=abrir_CADprodutos)
    botao_CADprodutos.pack(pady=10)

    # Espaço entre botões
    Label(janela_produtos, text="\n").pack()

    label_pedido = Label(janela_produtos, text="Digite o código do Produto:")
    label_pedido.pack()

    entrada_produto = Entry(janela_produtos)
    entrada_produto.pack()

    # Botão de pesquisa de produto
    botao_pesquisar = Button(janela_produtos, text="Pesquisar", command=pesquisar_produto)
    botao_pesquisar.pack()

    # Área de texto para mostrar o resultado da consulta
    texto_resultado = Text(janela_produtos, height=10, width=80)
    texto_resultado.pack()






def abrir_pedidos():
    janela_pedidos = Toplevel(janela)
    janela_pedidos.title("Pedidos")
    Label(janela_pedidos, text="->>> Aqui você pode cadastrar e pesquisar Pedidos <<<- \n").pack()

    def abrir_CADpedidos():
        janela_cad_pedidos = Toplevel()
        janela_cad_pedidos.title("Cadastro de Pedidos")
        Label(janela_cad_pedidos, text="->>> Tela para cadastrar novos pedidos <<<- \n").pack()

        # Lista para armazenar os produtos do pedido
        produtos_pedido = []

        # Variáveis globais para armazenar os menus de clientes e produtos
        dropdown_cliente = None
        dropdown_produto = None

        # Função para limpar todos os campos
        def limpar_campos():
            id_cliente_entry.delete(0, END)
            cod_produto_entry.delete(0, END)
            quantidade_entry.delete(0, END)
            valor_total_entry.delete(0, END)
            produtos_adicionados.delete(1.0, END)

        # Função para pesquisa dinâmica do cliente
        def pesquisar_cliente(event):
            nonlocal dropdown_cliente  # Permite modificar o menu de clientes fora do escopo interno
            if len(id_cliente_entry.get()) >= 3:
                query_cliente = "SELECT ID_Cliente, Nome_Cliente FROM Clientes WHERE Nome_Cliente ILIKE %s;"
                nome_cliente = f"%{id_cliente_entry.get()}%"
                resultados_clientes = Conexao_BD(query_cliente, (nome_cliente,))

                if resultados_clientes:
                    # Remove o menu anterior, se existir
                    if dropdown_cliente:
                        dropdown_cliente.destroy()

                    cliente_selecionado = StringVar(janela_cad_pedidos)
                    cliente_selecionado.set("Selecione o cliente")
                    dropdown_cliente = OptionMenu(janela_cad_pedidos, cliente_selecionado,
                                                  *[f"{r[1]} (ID: {r[0]})" for r in resultados_clientes])
                    dropdown_cliente.pack()

                    def cliente_selecionado_action(*args):
                        id_cliente_entry.delete(0, END)
                        id_cliente_entry.insert(0, cliente_selecionado.get().split("(ID: ")[1][
                                                   :-1])  # Extrai o ID do Cliente

                    cliente_selecionado.trace("w", cliente_selecionado_action)

        # Função para pesquisa dinâmica do produto
        def pesquisar_produto(event):
            nonlocal dropdown_produto  # Permite modificar o menu de produtos fora do escopo interno
            if len(cod_produto_entry.get()) >= 3:
                query_produto = "SELECT Cod_Produto, Nome_Produto FROM Produtos WHERE Nome_Produto ILIKE %s;"
                nome_produto = f"%{cod_produto_entry.get()}%"
                resultados_produtos = Conexao_BD(query_produto, (nome_produto,))

                if resultados_produtos:
                    # Remove o menu anterior, se existir
                    if dropdown_produto:
                        dropdown_produto.destroy()

                    produto_selecionado = StringVar(janela_cad_pedidos)
                    produto_selecionado.set("Selecione o produto")
                    dropdown_produto = OptionMenu(janela_cad_pedidos, produto_selecionado,
                                                  *[f"{r[1]} (ID: {r[0]})" for r in resultados_produtos])
                    dropdown_produto.pack()

                    def produto_selecionado_action(*args):
                        cod_produto_entry.delete(0, END)
                        cod_produto_entry.insert(0, produto_selecionado.get().split("(ID: ")[1][
                                                    :-1])  # Extrai o ID do Produto

                    produto_selecionado.trace("w", produto_selecionado_action)

        # Função para calcular o valor total do produto automaticamente
        def calcular_valor_total(event):
            try:
                quantidade = int(quantidade_entry.get())
                query_valor_produto = "SELECT Valor FROM Produtos WHERE Cod_Produto = %s;"
                resultado = Conexao_BD(query_valor_produto, (cod_produto_entry.get(),))
                if resultado:
                    valor_unitario = resultado[0][0]
                    valor_total = quantidade * valor_unitario
                    valor_total_entry.delete(0, END)
                    valor_total_entry.insert(0, f"{valor_total:.2f}")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida. Insira um número válido.")

        # Função para adicionar produtos à lista temporária
        def adicionar_produto():
            cod_produto = cod_produto_entry.get()
            quantidade = quantidade_entry.get()
            valor_total = valor_total_entry.get()

            # Adiciona os dados do produto à lista de produtos do pedido
            produtos_pedido.append((cod_produto, quantidade, valor_total))

            # Limpa os campos de produto para novas entradas
            cod_produto_entry.delete(0, END)
            quantidade_entry.delete(0, END)
            valor_total_entry.delete(0, END)

            # Atualiza a interface para mostrar os produtos adicionados
            produtos_adicionados.insert(END, f"Produto: {cod_produto}, Quantidade: {quantidade}, Valor: {valor_total}\n")

        # Função para cadastrar o pedido no banco de dados
        def cadastrar_pedido():
            id_cliente = id_cliente_entry.get()
            data_pagamento = data_pagamento_entry.get()

            # Se o campo de data de pagamento estiver vazio, usa o padrão do banco (data atual)
            if not data_pagamento:
                data_pagamento_convertida = None  # Deixa o banco de dados inserir o padrão (CURRENT_DATE)
            else:
                try:
                    data_pagamento_convertida = datetime.strptime(data_pagamento, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Erro", "Formato da data de pagamento inválido. Use o formato dd/mm/yyyy.")
                    return

            data_pedido_convertida = datetime.now().strftime("%Y-%m-%d")

            try:
                conexao = psycopg2.connect(
                    host="localhost",
                    database="Vendedores_de_Cosmeticos",
                    user="admin",
                    password="a123"
                )
                cursor = conexao.cursor()

                if data_pagamento_convertida:
                    query_pedido = """
                        INSERT INTO Pedidos (ID_Cliente, Data_Pedido, Data_Pagamento)
                        VALUES (%s, %s, %s)
                        RETURNING Cod_Pedido;
                    """
                    cursor.execute(query_pedido, (id_cliente, data_pedido_convertida, data_pagamento_convertida))
                else:
                    query_pedido = """
                        INSERT INTO Pedidos (ID_Cliente, Data_Pedido)
                        VALUES (%s, %s)
                        RETURNING Cod_Pedido;
                    """
                    cursor.execute(query_pedido, (id_cliente, data_pedido_convertida))

                cod_pedido = cursor.fetchone()[0]

                query_produto = """
                    INSERT INTO Pedido_Produtos (Cod_Pedido, Cod_Produto, Quantidade, Valor)
                    VALUES (%s, %s, %s, %s);
                """
                for produto in produtos_pedido:
                    cursor.execute(query_produto, (cod_pedido, produto[0], produto[1], produto[2]))

                conexao.commit()
                messagebox.showinfo("Sucesso", "Pedido cadastrado com sucesso!")
                limpar_campos()  # Limpa os campos após o cadastro

            except (Exception, psycopg2.DatabaseError) as error:
                conexao.rollback()
                messagebox.showerror("Erro", f"Erro ao cadastrar o pedido: {error}")
            finally:
                if conexao:
                    cursor.close()
                    conexao.close()

            # Função para buscar o próximo código de pedido disponível
            def obter_proximo_codigo_pedido():
                try:
                    conexao = psycopg2.connect(
                        host="localhost",
                        database="Vendedores_de_Cosmeticos",
                        user="admin",
                        password="a123"
                    )
                    cursor = conexao.cursor()

                    query_codigo = "SELECT COALESCE(MAX(Cod_Pedido), 0) + 1 FROM Pedidos;"
                    cursor.execute(query_codigo)
                    proximo_codigo = cursor.fetchone()[0]

                    return proximo_codigo
                except (Exception, psycopg2.DatabaseError) as error:
                    messagebox.showerror("Erro", f"Erro ao obter o próximo código de pedido: {error}")
                    return None
                finally:
                    if conexao:
                        cursor.close()
                        conexao.close()

        # Função para buscar o próximo código de pedido disponível
        def obter_proximo_codigo_pedido():
            try:
                conexao = psycopg2.connect(
                    host="localhost",
                    database="Vendedores_de_Cosmeticos",
                    user="admin",
                    password="a123"
                )
                cursor = conexao.cursor()

                query_codigo = "SELECT COALESCE(MAX(Cod_Pedido), 0) + 1 FROM Pedidos;"
                cursor.execute(query_codigo)
                proximo_codigo = cursor.fetchone()[0]

                return proximo_codigo
            except (Exception, psycopg2.DatabaseError) as error:
                messagebox.showerror("Erro", f"Erro ao obter o próximo código de pedido: {error}")
                return None
            finally:
                if conexao:
                    cursor.close()
                    conexao.close()

        # Campos de entrada
        Label(janela_cad_pedidos, text="Código do Pedido:").pack()
        proximo_cod_pedido = obter_proximo_codigo_pedido()
        cod_pedido_label = Label(janela_cad_pedidos, text=str(proximo_cod_pedido))
        cod_pedido_label.pack()

        Label(janela_cad_pedidos, text="Data do Pedido:").pack()
        data_pedido_atual = datetime.now().strftime("%d/%m/%Y")
        Label(janela_cad_pedidos, text=data_pedido_atual).pack()

        Label(janela_cad_pedidos, text="\n ID do Cliente:").pack()
        id_cliente_entry = Entry(janela_cad_pedidos)
        id_cliente_entry.pack()
        id_cliente_entry.bind("<KeyRelease>", pesquisar_cliente)

        Label(janela_cad_pedidos, text="Código do Produto:").pack()
        cod_produto_entry = Entry(janela_cad_pedidos)
        cod_produto_entry.pack()
        cod_produto_entry.bind("<KeyRelease>", pesquisar_produto)

        Label(janela_cad_pedidos, text="Quantidade:").pack()
        quantidade_entry = Entry(janela_cad_pedidos)
        quantidade_entry.pack()

        quantidade_entry.bind("<FocusOut>", calcular_valor_total)

        Label(janela_cad_pedidos, text="Valor Total do Produto:").pack()
        valor_total_entry = Entry(janela_cad_pedidos)
        valor_total_entry.pack()

        Label(janela_cad_pedidos, text="\n DATA DO PAGAMENTO \n(opcional dd/mm/yyyy):").pack()
        data_pagamento_entry = Entry(janela_cad_pedidos)
        data_pagamento_entry.pack()

        # Espaço entre botões
        Label(janela_cad_pedidos, text="\n").pack()

        Button(janela_cad_pedidos, text="Adicionar Produto +", command=adicionar_produto).pack(pady=10)

        produtos_adicionados = Text(janela_cad_pedidos, height=10, width=80)
        produtos_adicionados.pack()

        # Botão para cadastrar o pedido
        botao_cadastrar = Button(janela_cad_pedidos, text="Cadastrar Pedido", command=cadastrar_pedido)
        botao_cadastrar.pack(pady=10)


    # Função de pesquisa do pedido
    def pesquisar_pedido():
        global Pesq_pedido
        cod_pedido = entrada_pedido.get()

        if cod_pedido.isdigit():
            query = """
                SELECT
                    p.Cod_Pedido,
                    c.Nome_Cliente,
                    p.Data_Pedido,
                    pr.Nome_Produto,
                    pr.Valor,
                    pp.Quantidade,
                    (pp.Quantidade * pr.Valor) AS Valor_X_QT,
                    pp.Valor AS Valor_Total_Lançado,
                    (pp.Valor - pp.Quantidade * pr.Valor) AS Diferença,
                    SUM(pp.Valor) OVER (PARTITION BY p.Cod_Pedido) AS Valor_Total_Pedido,
                    p.Data_Pagamento
                FROM 
                    Pedidos p
                JOIN 
                    Clientes c ON p.ID_Cliente = c.ID_Cliente
                JOIN 
                    Pedido_Produtos pp ON p.Cod_Pedido = pp.Cod_Pedido
                JOIN 
                    Produtos pr ON pp.Cod_Produto = pr.Cod_Produto
                WHERE 
                    p.Cod_Pedido = %s;
                """
            resultados = Conexao_BD(query, cod_pedido)
        else:
            if (Pesq_pedido == "ASC"):
                query = """
                        SELECT
                            p.Cod_Pedido,
                            c.Nome_Cliente,
                            p.Data_Pedido,
                            pr.Nome_Produto,
                            pr.Valor,
                            pp.Quantidade,
                            (pp.Quantidade * pr.Valor) AS Valor_X_QT,
                            pp.Valor AS Valor_Total_Lançado,
                            (pp.Valor - pp.Quantidade * pr.Valor) AS Diferença,
                            SUM(pp.Valor) OVER (PARTITION BY p.Cod_Pedido) AS Valor_Total_Pedido,
                            p.Data_Pagamento
                        FROM 
                            Pedidos p
                        JOIN 
                            Clientes c ON p.ID_Cliente = c.ID_Cliente
                        JOIN 
                            Pedido_Produtos pp ON p.Cod_Pedido = pp.Cod_Pedido
                        JOIN 
                            Produtos pr ON pp.Cod_Produto = pr.Cod_Produto
                        ORDER BY 
                            p.Cod_Pedido ASC;
                        """
                resultados = Conexao_BD(query)
                Pesq_pedido = "DESC"
            else:
                query = """
                        SELECT
                            p.Cod_Pedido,
                            c.Nome_Cliente,
                            p.Data_Pedido,
                            pr.Nome_Produto,
                            pr.Valor,
                            pp.Quantidade,
                            (pp.Quantidade * pr.Valor) AS Valor_X_QT,
                            pp.Valor AS Valor_Total_Lançado,
                            (pp.Valor - pp.Quantidade * pr.Valor) AS Diferença,
                            SUM(pp.Valor) OVER (PARTITION BY p.Cod_Pedido) AS Valor_Total_Pedido,
                            p.Data_Pagamento
                        FROM 
                            Pedidos p
                        JOIN 
                            Clientes c ON p.ID_Cliente = c.ID_Cliente
                        JOIN 
                            Pedido_Produtos pp ON p.Cod_Pedido = pp.Cod_Pedido
                        JOIN 
                            Produtos pr ON pp.Cod_Produto = pr.Cod_Produto
                        ORDER BY 
                            p.Cod_Pedido DESC;
                                    """
                resultados = Conexao_BD(query)
                Pesq_pedido = "ASC"

        if resultados:
            texto_resultado.delete(1.0, END)
            total_resultados = len(resultados)

            if cod_pedido.isdigit():
                for index, row in enumerate(resultados):
                    if index == 0:
                        texto_resultado.insert(END,
                                               f"Pedido: {row[0]}, Cliente: {row[1]}, Data do Pedido: {row[2]}, \n\n")
                    texto_resultado.insert(END,
                                           f"Produto: {row[3]} \n Valor UN: {row[4]}, QT: {row[5]}, Total: {row[6]} \n Valor Lançado: {row[7]}, Diferença: {row[8]} \n\n")
                    if index == total_resultados - 1:
                        texto_resultado.insert(END,
                                               f"\n Valor Total: {row[9]}, Data do Pagamento: {row[10]}, \n\n")
            else:
                for index, row in enumerate(resultados):
                    texto_resultado.insert(END, f"Pedido: {row[0]}, Cliente: {row[1]}, Data do Pedido: {row[2]}, \n")
                    texto_resultado.insert(END, f"Produto: {row[3]}, Valor UN: {row[4]}, QT: {row[5]}, Total: {row[6]}, Valor Lançado: {row[7]}, Diferença: {row[8]},")
                    texto_resultado.insert(END, f"Valor Total: {row[9]}, Data do Pagamento: {row[10]}, \n\n")
        else:
            messagebox.showinfo("Resultado", "Nenhum pedido encontrado.")


    # Função para Ajustes da Data do Pagamento
    def abrir_DATApagamento():
        janela_DATApagamento = Toplevel()
        janela_DATApagamento.title("Ajustar Data de Pagamento")

        # Layout e explicação inicial
        Label(janela_DATApagamento, text="->>> Ajustar ou Pesquisar Data de Pagamento <<<- \n").pack()

        # Campo para inserir o número do pedido
        Label(janela_DATApagamento, text="Número do Pedido:").pack()
        entrada_numero_pedido = Entry(janela_DATApagamento)
        entrada_numero_pedido.pack()

        # Campo para inserir a nova data de pagamento
        Label(janela_DATApagamento, text="Nova Data de Pagamento (dd/mm/yyyy):").pack()
        entrada_data_pagamento = Entry(janela_DATApagamento)
        entrada_data_pagamento.pack()


        # Função para ajustar a data de pagamento de um pedido existente
        def ajustar_data_pagamento():
            numero_pedido = entrada_numero_pedido.get()
            data_pagamento = entrada_data_pagamento.get()

            if not numero_pedido:
                texto_resultado.insert(END, "Erro: Número do pedido é obrigatório para ajustar a data.\n")
                return

            if data_pagamento != "":
                try:
                    # Validar e converter a data de pagamento
                    nova_data_pagamento = datetime.strptime(data_pagamento, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    texto_resultado.insert(END, "Erro: Formato de data inválido. Use dd/mm/yyyy.\n")
                    return
            else:
                nova_data_pagamento = None

            # Query para atualizar a data de pagamento do pedido
            query_update = """
                UPDATE Pedidos
                SET Data_Pagamento = %s
                WHERE Cod_Pedido = %s;
            """
            try:
                conexao = psycopg2.connect(
                    host="localhost",
                    database="Vendedores_de_Cosmeticos",
                    user="admin",
                    password="a123"
                )
                cursor = conexao.cursor()
                cursor.execute(query_update, (nova_data_pagamento, numero_pedido))
                conexao.commit()

                if cursor.rowcount > 0:
                    texto_resultado.insert(END, f"Data de pagamento ajustada para o pedido {numero_pedido}.\n")
                else:
                    texto_resultado.insert(END, f"Nenhum pedido encontrado com o número {numero_pedido}.\n")

            except (Exception, psycopg2.DatabaseError) as error:
                texto_resultado.insert(END, f"Erro ao ajustar a data de pagamento: {error}\n")
            finally:
                if conexao:
                    cursor.close()
                    conexao.close()

        # Função para pesquisar pedidos
        # Função para pesquisar pedidos
        def pesquisar_pedido():
            numero_pedido = entrada_numero_pedido.get()
            data_pagamento = entrada_data_pagamento.get()

            # Caso nenhum número de pedido seja digitado, buscar todos os pedidos da data de pagamento
            if not numero_pedido and data_pagamento:
                try:
                    data_formatada = datetime.strptime(data_pagamento, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    texto_resultado.delete(1.0, END)
                    texto_resultado.insert(END, "Erro: Formato de data inválido. Use dd/mm/yyyy.\n")
                    return

                query_todos_pedidos = """
                    SELECT p.Cod_Pedido, c.Nome_Cliente, p.Data_Pedido, p.Data_Pagamento
                    FROM Pedidos p
                    JOIN Clientes c ON p.ID_Cliente = c.ID_Cliente
                    WHERE p.Data_Pagamento = %s;
                """
                try:
                    conexao = psycopg2.connect(
                        host="localhost",
                        database="Vendedores_de_Cosmeticos",
                        user="admin",
                        password="a123"
                    )
                    cursor = conexao.cursor()
                    cursor.execute(query_todos_pedidos, (data_formatada,))
                    resultados = cursor.fetchall()

                    if resultados:
                        texto_resultado.delete(1.0, END)
                        for pedido in resultados:
                            texto_resultado.insert(END, f"Pedido: {pedido[0]}, Cliente: {pedido[1]}\n "
                                                        f"Data Pedido: {pedido[2]}, Data Pagamento: {pedido[3]}\n\n")
                    else:
                        texto_resultado.delete(1.0, END)
                        texto_resultado.insert(END, "Nenhum pedido encontrado para a data de pagamento informada.\n")

                except (Exception, psycopg2.DatabaseError) as error:
                    texto_resultado.delete(1.0, END)
                    texto_resultado.insert(END, f"Erro ao pesquisar pedidos: {error}\n")
                finally:
                    if conexao:
                        cursor.close()
                        conexao.close()

            # Caso tenha número de pedido e data de pagamento, pesquisar pedidos sem data de pagamento (null)
            elif numero_pedido:
                query_sem_data_pagamento = """
                    SELECT p.Cod_Pedido, c.Nome_Cliente, p.Data_Pedido, p.Data_Pagamento
                    FROM Pedidos p
                    JOIN Clientes c ON p.ID_Cliente = c.ID_Cliente
                    WHERE p.Cod_Pedido = %s;
                """
                try:
                    conexao = psycopg2.connect(
                        host="localhost",
                        database="Vendedores_de_Cosmeticos",
                        user="admin",
                        password="a123"
                    )
                    cursor = conexao.cursor()
                    cursor.execute(query_sem_data_pagamento, (numero_pedido,))
                    resultados = cursor.fetchall()

                    if resultados:
                        texto_resultado.delete(1.0, END)
                        for pedido in resultados:
                            texto_resultado.insert(END, f"Pedido: {pedido[0]}, Cliente: {pedido[1]}\n "
                                                        f"Data Pedido: {pedido[2]}, Data Pagamento: {pedido[3]}\n")
                    else:
                        texto_resultado.delete(1.0, END)
                        texto_resultado.insert(END, f"Nenhum pedido encontrado para o número {numero_pedido}.\n")

                except (Exception, psycopg2.DatabaseError) as error:
                    texto_resultado.delete(1.0, END)
                    texto_resultado.insert(END, f"Erro ao pesquisar pedidos: {error}\n")
                finally:
                    if conexao:
                        cursor.close()
                        conexao.close()

            # Caso o usuário não insira nem número de pedido nem data de pagamento
            else:
                query_todos_pedidos = """
                    SELECT p.Cod_Pedido, c.Nome_Cliente, p.Data_Pedido, p.Data_Pagamento
                    FROM Pedidos p
                    JOIN Clientes c ON p.ID_Cliente = c.ID_Cliente
                    WHERE p.Data_Pagamento IS NULL;
                """
                try:
                    conexao = psycopg2.connect(
                        host="localhost",
                        database="Vendedores_de_Cosmeticos",
                        user="admin",
                        password="a123"
                    )
                    cursor = conexao.cursor()
                    cursor.execute(query_todos_pedidos)
                    resultados = cursor.fetchall()

                    if resultados:
                        texto_resultado.delete(1.0, END)
                        for pedido in resultados:
                            texto_resultado.insert(END, f"Pedido: {pedido[0]}, Cliente: {pedido[1]} \n "
                                                        f"Data Pedido: {pedido[2]}, Data Pagamento: {pedido[3]}\n\n")
                    else:
                        texto_resultado.delete(1.0, END)
                        texto_resultado.insert(END, "Nenhum pedido encontrado com data de pagamento pendente (null).\n")

                except (Exception, psycopg2.DatabaseError) as error:
                    texto_resultado.delete(1.0, END)
                    texto_resultado.insert(END, f"Erro ao pesquisar pedidos: {error}\n")
                finally:
                    if conexao:
                        cursor.close()
                        conexao.close()

        botao_pesquisar = Button(janela_DATApagamento, text="Pesquisar Pedido", command=pesquisar_pedido)
        botao_pesquisar.pack(pady=10)

        # Área de texto para exibir os resultados
        texto_resultado = Text(janela_DATApagamento, height=10, width=80)
        texto_resultado.pack()

        # Botões para ajustar a data de pagamento e pesquisar o pedido
        botao_ajustar = Button(janela_DATApagamento, text="Ajustar Data", command=ajustar_data_pagamento)
        botao_ajustar.pack(pady=10)



    # Botão de cadastro de pedidos
    botao_CADpedidos = Button(janela_pedidos, text="+ Pedidos +", command=abrir_CADpedidos)
    botao_CADpedidos.pack(pady=10)

    # Botão de ajuste da Data do Pagamento
    botao_DATApagamento = Button(janela_pedidos, text="🖍  Data de Pagamento 🖍 ", command=abrir_DATApagamento)
    botao_DATApagamento.pack(pady=10)

    # Espaço entre botões
    Label(janela_pedidos, text="\n").pack()

    label_pedido = Label(janela_pedidos, text="Digite o código do Pedido:")
    label_pedido.pack()

    entrada_pedido = Entry(janela_pedidos)
    entrada_pedido.pack()

    # Botão de pesquisa de pedidos
    botao_pesquisar = Button(janela_pedidos, text="Pesquisar", command=pesquisar_pedido)
    botao_pesquisar.pack()


    # Área de texto para mostrar o resultado da consulta
    texto_resultado = Text(janela_pedidos, height=10, width=80)
    texto_resultado.pack()






# Função para centralizar a janela
def centralizar_janela(largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

# Interface gráfica principal
janela = Tk()
janela.title("Sistema de Vendas e Relatório")

# Definir tamanho e centralizar janela
centralizar_janela(400, 300)

# Espaço entre botões
Label(janela, text="\n").pack()

# Espaço entre botões
Label(janela, text="\n").pack()

# Botões da tela inicial
botao_clientes = Button(janela, text="1) CLIENTES", command=abrir_clientes)
botao_clientes.pack(pady=10)

botao_produtos = Button(janela, text="2) PRODUTOS", command=abrir_produtos)
botao_produtos.pack(pady=10)

botao_pedidos = Button(janela, text="3) > PEDIDOS <", command=abrir_pedidos)
botao_pedidos.pack(pady=10)

janela.mainloop()
