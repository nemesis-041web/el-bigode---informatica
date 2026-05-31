import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

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