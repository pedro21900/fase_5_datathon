import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

logging.info("Carregando dados...")
# Conectar ao banco de dados SQLite
engine = create_engine('sqlite:///data/refined/datawarehouse.db')

# Garantir a mesma ordem das colunas
colunas = ['history', 'url', 'issued', 'modified', 'title', 'body', 'caption',
           'recency_score', 'popularity_score']

# Carregar as tabelas 'merged_data' e 'news_item' no pandas
merged = pd.read_sql_table('merged_data', con=engine)
news_item = pd.read_sql_table('news_item', con=engine)

logging.info("Dado preparados com sucesso!")