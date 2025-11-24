import sys
import os
import mysql.connector
import csv

DB = mysql.connector.connect(
host="localhost",
user="root",
password=""
)

# Doesn't work currently--missing file
def import_(folder_name):
    mycursor = DB.cursor()
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        print(x)

def insertAgentClient(uid, username, email, card_number, card_holder, expiration_date, cvv, zip_code, interests):
    mycursor = DB.cursor()
    mycursor.execute("USE projectdb")

    sql = """
    INSERT INTO AgentClient 
    (uid, username, email, card_number, card_holder, expiration_date, cvv, interests)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        int(uid), 
        username, 
        email, 
        int(card_number), 
        card_holder, 
        expiration_date, 
        int(cvv), 
        int(zip_code), 
        interests
    )
    
    mycursor.execute(sql, values)
    mycursor.commit()

def main():
    # sys.argv
    # [0] - project.py 
    # [1] - (im)
    # [2] - Other Parameters
    print(f'COMMAND LINE ARGUMENTS --- {sys.argv}\n\n')
    command = sys.argv[1]


    if command == "import":
        import_(sys.argv[2])
    elif command == "insertAgentClient":
        insertAgentClient(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])

    

if __name__ == "__main__":
    main()