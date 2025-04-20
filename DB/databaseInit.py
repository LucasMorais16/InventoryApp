from .database_users import create_user_tables 
from .database_location import create_location_tables, populate_location_data
from .database_departments import create_departments_table, populate_departments_data
from .database_stockroom import create_stockroom_table
from .database_item_codes import create_item_codes_table, populate_item_codes_data
from .database_tokens import create_tokens_table
from .database_checklist import create_checklists_tables
from .database_checklist_template import create_checklist_templates_tables

def create_tables():
    create_user_tables()
    create_location_tables()
    populate_location_data()
    create_departments_table()      
    populate_departments_data()       
    create_stockroom_table()        
    create_item_codes_table()      
    populate_item_codes_data()      
    create_tokens_table()
    create_checklist_templates_tables()
    create_checklists_tables()
    