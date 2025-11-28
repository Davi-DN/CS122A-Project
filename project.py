import sys
import os
import mysql.connector
import csv

# CHANGE PASSWORD TO MATCH 
DB = mysql.connector.connect(
host="localhost",
user="root",
password=""
)

AGENT_PLATFORM = {
    "User": {
        "uid" : "INT",
        "email" : "TEXT",
        "username" : "TEXT"
    },  
    "AgentCreator" : {
        "uid": "INT",
        "bio": "TEXT",
        "payout": "TEXT"
    },
    "AgentClient": {
        "uid": "INT",
        "interests": "TEXT",
        "cardholder": "TEXT",
        "expire": "DATE",
        "cardno": "INT",
        "zip": "INT",
        "cvv": "INT"
    },
    "BaseModel": {
        "bmid": "INT",
        "description": "TEXT",
        "creator_uid": "TEXT"
    },
    "CustomizedModel": {
        "bmid": "INT",
        "mid": "INT"
    },
    "Configuration": {
        "cid": "INT",
        "client_uid": "INT",
        "content": "TEXT",
        "labels": "TEXT"
    },
    "InternetService": {
        "sid": "INT",
        "provider": "TEXT",
        "endpoints": "TEXT"
    },
    "LLMService": {
        "sid": "INT",
        "domain": "TEXT"
    },
    "DataStorage": {
        "sid": "TEXT",
        "type": "TEXT"
    },
    "ModelServices": {
        "bmid": "INT",
        "sid": "INT",
        "version": "INT"
    },
    "ModelConfigurations": {
        "bmid": "INT",
        "mid": "INT",
        "cid": "INT",
        "duration": "INT"
    }
}

def import_(folder_name):
    mycursor = DB.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS projectdb")
    mycursor.execute("USE projectdb")

    for table in os.listdir(folder_name):
        table_name = os.path.splitext(table)[0]

        mycursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        create_table = ", ".join(f"{item} {item_type}" for item, item_type in AGENT_PLATFORM[table_name].items())
        mycursor.execute(f"CREATE TABLE {table_name} ({create_table})")

        with open(os.path.join(folder_name, table), newline="") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            
            columns = list(AGENT_PLATFORM[table_name].keys())
            column_add = ", ".join(columns)
            value_placeholders = ", ".join(["%s"] * len(columns))
            insert = f"INSERT INTO {table_name} ({column_add}) VALUES ({value_placeholders})"

            for row in csv_reader:
                mycursor.execute(insert, tuple(row))

            DB.commit()

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
    DB.commit()

    print("Success") if mycursor.rowcount == 1 else print("Fail")

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
    DB.commit()

    print("Success") if mycursor.rowcount == 1 else print("Fail")

def deleteBaseModel(bmid):
    mycursor = DB.cursor()
    mycursor.execute("USE projectdb")

    sql = """
    DELETE FROM BaseModel 
    WHERE bmid = %s
    """
    mycursor.execute(sql, int(bmid))
    DB.commit()

    print("Success") if mycursor.rowcount > 0 else print("Fail")


def listInternetService(bmid):
    mycursor = DB.cursor()
    mycursor.execute("USE projectdb")

    sql = """
    SELECT sid, endpoint, provider FROM InternetService 
    WHERE bmid = %s
    ORDER BY provider ASC
    """
    mycursor.execute(sql, int(bmid))
    table = mycursor.fetchall()

    for row in table:
        print(",".join(str(column) for column in row))

def main():
    # sys.argv
    # [0] - project.py 
    # [1] - (im)
    # [2] - Other Parameters
    print(f'COMMAND LINE ARGUMENTS --- {sys.argv}\n')
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
        print("Database not found!", exc)


if __name__ == "__main__":
    main()