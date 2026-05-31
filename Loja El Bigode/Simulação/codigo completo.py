import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from faker import Faker
import faker_commerce
import sqlite3
import random

# Inicializando a biblioteca e ativando o provedor de E-commerce, focado em produtos.
fake = Faker()
fake.add_provider(faker_commerce.Provider)

# Criando o banco de dados e se conectando a ele
nome_banco = "loja_elbigode.db"
conexao = sqlite3.connect(nome_banco)
cursor = conexao.cursor()

query_criacao= """
CREATE TABLE IF NOT EXISTS estoque (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  quantidade INTEGER,
  preco REAL
);
"""
# Este Try serve pro código continuar, mesmo que ocorra erros <NA CRIAÇÃO DA TABELA>
try:
  cursor.execute(query_criacao)
  conexao.commit()
  print("Deu bom! A tabela 'estoque' foi criada perfeitamente meu mano!")

# =======================================================
# OBS1: Aqui é onde vou encher de dados falsos.
# Por isso, criei a condição para prevenir erros:
# Somente se o banco tiver nada, que irei aplicar a massa de dados falsos.
  cursor.execute("SELECT COUNT(*) FROM estoque")
  if cursor.fetchone()[0] == 0:
    print("Banco de dados está vazio... Gerando 50 produtos fictícios...")

    query_inserir = """
    INSERT INTO estoque (nome, quantidade, preco)
    VALUES (?, ?, ?);
    """
# Enumerei os valores de cada coluna para as linhas que adicionarei e... Laço!
    for _ in range(50):
      nome_produto = fake.ecommerce_name()
# a biblioteca padrão random!! Usei pra preencher outras colunas com uma taxa aleatória!
      quantidade = random.randint(1,100)
      preco = round(
          random.uniform(5.00, 5000.00), 2
      )
      cursor.execute(query_inserir, (nome_produto, quantidade, preco))
  conexao.commit()
  print("Adicionamos os produtos fictícios com sucesso!")

except sqlite3.Error as e:
  print(f"Num deu pra preencher essa tabela devido a este erro: {e}")
  conexao.rollback()


finally:
  conexao.close()
  print("Conexão encerrada com segurança!")

def carregar_dados_banco():
    try:
        # LIMPA
        for item in tabela_db.get_children():
            tabela_db.delete(item)

        # 2. Conecta ao banco de dados relacional
        conexao = sqlite3.connect("loja_elbigode.db")
        cursor = conexao.cursor()

        # 3. Busca os dados reais gravados na tabela 'estoque'
        cursor.execute("SELECT id, nome, quantidade, preco FROM estoque")
        linhas = cursor.fetchall() # Retorna uma lista de tuplas

        # 4. Percorre os dados e joga tudo para dentro do Treeview
        for linha in linhas:
            # linha[0] = id, linha[1] = nome, linha[2] = quantidade, linha[3] = preco
            tabela_db.insert("", tk.END, values=(linha[0], linha[1], linha[2], f"R$ {linha[3]:.2f}"))

        conexao.close()
    except Exception as e:
        messagebox.showerror("Erro de Banco", f"Não foi possível ler os dados: {e}")


def adicionar_produto():
  # O que foi escrito na entrada? Vamos pegar!
  add_nome = entry_nome.get()
  add_qtd= entry_qtd.get()
  add_preco= entry_preco.get()

  # Agora sim, vamos tratar esses dados que estão querendo chegar ao banco!
  nome_tratado = add_nome.strip().title()
  # strip remove espaços vazios nos extremos e title faz toda palavra começar UPPER

  # Teste de Validação: Proibido ter nada no campo do nome
  if not nome_tratado:
    messagebox.showwarning("Nome - Erro!", "ESTE CAMPO NÃO PODE FICAR ASSIM! ESCREVA ALGO!")
    return

  # Tratamento de Tipo de Dado: Quantidade
  try:
    qtd_tratada = int(add_qtd)
    if qtd_tratada < 0:
      raise ValueError
  except ValueError:
    messagebox.showerror("Quantidade - Erro de Digitação!", "Escreva um número positivo!")
    return

  # Tratamento de Tipo de Dado: Preço
  try:
    preco_limpo = add_preco.replace(",", ".")
    preco_tratado = float(preco_limpo)
    if preco_tratado < 0:
      raise ValueError
  except ValueError:
    messagebox.showerror("Preço - Erro de Digitação!", "Insira um preço válido! (como 15,50)")
    return

  # Agora que tratamos os dados, vamos deixar que cheguem ao banco!
  try:
    conexao = sqlite3.connect(nome_banco)
    cursor = conexao.cursor()

    query_inserir = """
    INSERT INTO estoque (nome, quantidade, preco)
    VALUES( ?, ?, ?);
    """

    cursor.execute(query_inserir, (nome_tratado, qtd_tratada, preco_tratado))
    conexao.commit()
    conexao.close()

    messagebox.showinfo("O produto ", f"'{nome_tratado}' foi adicionado com sucesso!")

    # Por fim, vamos limpar os campos após a adição e atualizar o banco!
    entry_nome.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_id.delete(0, tk.END)

    carregar_dados_banco()
  except Exception as e:
    messagebox.showerror("ERRO!", f"Não foi possível adicionar devido a {e}")


# (ESTA PARTE FOI CRIADA TOTALMENTE UTILIZANDO COMO REFERÊNCIA OS CÓDIGOS DO PROF)
janela_sistema = tk.Tk()
janela_sistema.title("Loja El Bigode")
janela_sistema.geometry("600x350")

tk.Label(janela_sistema, text="Produtos armazenados no banco de dados", font=("Arial", 12, "bold")).pack(pady=10)

# Campos para entrada de dados:
frame_campos = tk.Label(janela_sistema)
# frame é tipo uma forma de agrupar, separar algo. Coloquei acima da tabela
frame_campos.pack(pady=10, fill="x", padx=10)

# ID
entry_id = tk.Entry(frame_campos) #escondido. pq...

# Nome
tk.Label(frame_campos, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_campos, width=25)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

# Quantidade
tk.Label(frame_campos, text="Quantidade:").grid(row=0, column=2, padx=5, pady=5)
entry_qtd = tk.Entry(frame_campos, width=8)
entry_qtd.grid(row=0, column=3, padx=5, pady=5)

# Preço
tk.Label(frame_campos, text="Preço (R$):").grid(row=0, column=4, padx=5, pady=5)
entry_preco = tk.Entry(frame_campos, width=10)
entry_preco.grid(row=0, column=5, padx=5, pady=5)

# Finalmente, criando o Treeview para as 4 colunas do banco:
tabela_db = ttk.Treeview(janela_sistema, columns=("id", "nome", "qtd", "preco"), show="headings")

tabela_db.heading("id", text="ID")
tabela_db.heading("nome", text="Nome do Produto")
tabela_db.heading("qtd", text="Qtd em Estoque")
tabela_db.heading("preco", text="Preço Unitário")

tabela_db.column("id", width=50, anchor="center")
tabela_db.column("nome", width=220, anchor="w")
tabela_db.column("qtd", width=100, anchor="center")
tabela_db.column("preco", width=120, anchor="center")

tabela_db.pack(pady=10, fill="both", expand=True)

# Botão Adicionar
btn_add = tk.Button(janela_sistema, text="Adicionar Produto", command=adicionar_produto)
btn_add.pack(pady=10)

carregar_dados_banco()

janela_sistema.mainloop()
