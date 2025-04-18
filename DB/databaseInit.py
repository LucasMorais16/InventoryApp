from .database_users import create_user_tables 
from .database_location import create_location_tables, populate_location_data
from .database_departments import create_departments_table, populate_departments_data
from .database_stockroom import create_stockroom_table
from .database_item_codes import create_item_codes_table, populate_item_codes_data
from .database_tokens import create_tokens_table

def create_tables():
    # Cria as tabelas de usuários, localizações e departamentos
    create_user_tables()
    create_location_tables()
    populate_location_data()
    create_departments_table()      # Cria a tabela de departamentos
    populate_departments_data()     # Popula a tabela de departamentos
    
    # Cria as tabelas de estoque e códigos dos itens
    create_stockroom_table()        # Cria a tabela de estoque (stockroom)
    create_item_codes_table()       # Cria a tabela dos códigos dos itens
    populate_item_codes_data()      # Popula a tabela dos códigos dos itens
    create_tokens_table()