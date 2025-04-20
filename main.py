from DB.databaseInit import create_tables
from gui import login_window

if __name__ == "__main__":
    create_tables()    
    login_window() 