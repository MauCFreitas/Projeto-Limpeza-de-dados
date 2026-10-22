from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://postgres:123@localhost:5432/PROJETO_LIMPEZA_DADOS"
)

clientes = pd.read_csv(f"projeto_limpeza_dados\DATA\CLEAN\clientes_clean.csv")
produtos = pd.read_csv(f"projeto_limpeza_dados\DATA\CLEAN\produtos_clean.csv")
pedidos = pd.read_csv(f"projeto_limpeza_dados\DATA\CLEAN\pedidos_clean.csv")
itens = pd.read_csv(f"projeto_limpeza_dados\DATA\CLEAN\itens_clean.csv")

clientes.to_sql(
    "clientes",
    engine,
    if_exists="replace",
    index=False
)
