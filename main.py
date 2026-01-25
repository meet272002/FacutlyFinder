from dbOperations.tables_create import CreateTable
from dbOperations.tables_insert import InsertValues
from dbConnection.db_connection import SQLConnection as sc
from contextlib import closing
from preprocess.preprocess import PreProcess as pp


def main():
    conn = sc()
    connection = conn.getConnection()
    # print(connection[0].cursor())

    
    if connection[1] == 1:
        with closing(connection[0]) as con:
            pre_process = pp()
            pre_process.faculty()
            print("Preprocessing Done")

            table_creator = CreateTable(con)
            table_creator.create_tables()
            print("Tables Created")

            insert_value = InsertValues(con)
            insert_value.insert_values()
            print("Values Inserted")
    else:
        print("Error in Database Connection")
if __name__ == "__main__":
    main()
