import sys
import mysql.connector

def import_(db, folder_name):

    print(f'Foldername - {folder_name}')
    
    mycursor = db.cursor()
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        print(x)
    
def main():
    # sys.argv
    # [0] - project.py 
    # [1] - (function command)
    # [2] - Other Parameters
    command = sys.argv[1]

    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
    )

    if command == "import":
        import_(db, sys.argv[2])

    

if __name__ == "__main__":
    main()
