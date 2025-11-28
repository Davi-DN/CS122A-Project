import sys
import os
import mysql.connector
import csv

DB = mysql.connector.connect(
host="localhost",
user="root",
password="mysQL5%"
)

def import_(folder_name):
    mycursor = DB.cursor()
    mycursor.execute("SHOW CREATE DATABASE IF NOT EXISTS projectdb")



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

def addCustomizedModel(mid, bmid):
    mycursor = DB.cursor()
    mycursor.execute("USE projectdb")

    sql = """
    INSERT INTO CustomizedModel 
    (mid, bmid)
    VALUES (%s, %s)
    """
    values = (
        int(mid), 
        int(bmid)
    )

    mycursor.execute(sql, values)
    mycursor.commit()

    return True if mycursor.rowcount == 1 else False

def deleteBaseModel(bmid):
    mycursor = DB.cursor()
    mycursor.execute("USE projectdb")

    sql = """
    DELETE FROM BaseModel 
    WHERE bmid = %s
    """
    mycursor.execute(sql, int(bmid))
    mycursor.commit()

    return True if mycursor.rowcount > 0 else False


def listInternetService(bmid):
    mycursor = DB.cursor()
    mycursor.execute("USE projectdb")

    sql = """
    SELECT sid, endpoint, provider FROM InternetService 
    WHERE bmid = %s
    ORDER BY provider ASC
    """
    mycursor.execute(sql, int(bmid))
    return mycursor.fetchall()




def main():
    # sys.argv
    # [0] - project.py 
    # [1] - (im)
    # [2] - Other Parameters
    print(f'COMMAND LINE ARGUMENTS --- {sys.argv}\n\n')
    command = sys.argv[1]

    try:
        match command:
            case "import":
                import_(sys.argv[2])
            case "insertAgentClient":
                insertAgentClient(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
            case "addCustomizedModel":
                addCustomizedModel(sys.argv[2], sys.argv[3])
            case "deleteBaseModel":
                deleteBaseModel(sys.argv[2])
            case "listInternetService":
                listInternetService(sys.argv[2])
    except mysql.connector.ProgrammingError as exc:
        print("Database not found!")


if __name__ == "__main__":
    main()