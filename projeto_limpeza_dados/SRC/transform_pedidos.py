import pandas as pd
import numpy as np
import re

# para esta correção de tabela, precisarei usar todas as outras tabelas ja organizadas

clientes = pd.read_csv(f'projeto_limpeza_dados\DATA\CLEAN\clientes_clean.csv')
itens = pd.read_csv(f'projeto_limpeza_dados\DATA\CLEAN\itens_clean.csv')
produtos = pd.read_csv(f'projeto_limpeza_dados\DATA\CLEAN\produtos_clean.csv')
pedidos = pd.read_csv(f"projeto_limpeza_dados\DATA\RAW\pedidos.csv")

print(pedidos.head())
print(pedidos.info())
print(pedidos.isna().sum())



# para iniciar, preciso corrigir todos os valores que estão incorretos

######### CORRIGINDO AS DATAS

pedidos["data_pedido"] = pd.to_datetime(pedidos["data_pedido"], errors="coerce")
pedidos["data_pedido"] = pedidos["data_pedido"].dt.strftime('%d/%m/%Y')

# algumas datas ficaram nulas neste processo e precisarão ser apagadas

pedidos = pedidos.dropna(
    subset=["data_pedido"]
)

######### CORRIGINDO OS STATUS

pedidos["status"] = pedidos["status"].replace({
    "delivered" : "entregue"
})


pedidos["status"] = (
    pedidos["status"]
    .str.title()
    .str.strip()
)

######### VERIFICANDO SE DATA PEDIDO E DATA DE CADASTRO

# as datas dos pedidos não podem preceder as datas de cadastro dos clientes, para isso, preciso fazer uma checagem

comparacao = pedidos.merge(
    clientes[["id_cliente", "data_cadastro"]],
    on="id_cliente",
    how="left"
)

pedidos_invalidos = comparacao.loc[
    comparacao["data_pedido"] < comparacao["data_cadastro"],
    "id_cliente"
] 

pedidos.loc[
    pedidos["id_pedido"].isin(pedidos_invalidos),
    "data_pedido"
] = clientes["data_cadastro"]

# eu pensei em cancelar todos os pedidos que apresentassem data inferior a data de cadastro, mas isto resultou em muitas datas invalidas
# então decidi corrigir as datas dos pedidos para que ficassem equivalentes as datas dos cadastros de clientes

pedidos.to_csv(
r"projeto_limpeza_dados\DATA\CLEAN\pedidos_clean.csv",
index=False,
encoding="utf-8-sig"
)