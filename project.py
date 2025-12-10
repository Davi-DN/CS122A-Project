import sys
import os
import mysql.connector
import csv

def connection():
    return mysql.connector.connect(
host="localhost",
user="test",
password="password",
database="cs122a"
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
        "cardno": "BIGINT",
        "cvv": "INT",
        "zip": "INT"
    },
    "BaseModel": {
        "bmid": "INT",
        "creator_uid": "INT",
        "description": "TEXT"
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
        "sid": "INT",
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
    db = connection()
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS cs122a")
    mycursor.execute("USE cs122a")

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

    print("Success") if mycursor.rowcount == 1 else print("Fail")
    db.commit() 
    db.close()


def insertAgentClient(uid, username, email, card_number, card_holder, expiration_date, cvv, zip_code, interests):
    db = connection()
    mycursor = db.cursor()
    mycursor.execute("SELECT 1 FROM AgentClient WHERE uid = %s", (uid,))
    result = mycursor.fetchone()
    if result:
        print("Fail")
        return

    sql_agent_client = """
    INSERT INTO AgentClient 
    (uid, cardno, cardholder, expire, cvv, zip, interests)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values_agent_client = (
        int(uid), 
        int(card_number), 
        card_holder, 
        expiration_date, 
        int(cvv), 
        int(zip_code), 
        interests
    )
    
    sql_user = """
    INSERT INTO User 
    (uid, username, email)
    VALUES (%s, %s, %s)
    """
    values_user = (int(uid), username, email)

    mycursor.execute(sql_agent_client, values_agent_client)
    mycursor.execute(sql_user, values_user)
    db.commit()
    db.close()

    print("Success") if mycursor.rowcount == 1 else print("Fail")

def addCustomizedModel(mid, bmid):
    db = connection()
    mycursor = db.cursor()

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
    db.commit()
    db.close()

    print("Success") if mycursor.rowcount == 1 else print("Fail")

def deleteBaseModel(bmid):
    db = connection()
    mycursor = db.cursor()

    sql = """
    DELETE FROM BaseModel 
    WHERE bmid = %s
    """
    mycursor.execute(sql, [int(bmid)])
    db.commit()
    db.close()

    print("Success") if mycursor.rowcount > 0 else print("Fail")


def listInternetService(bmid):
    db = connection()
    mycursor = db.cursor()

    sql = """
    SELECT i.sid, i.endpoints, i.provider 
    FROM InternetService AS i
    JOIN ModelServices AS m ON i.sid = m.sid
    WHERE bmid = %s
    ORDER BY provider ASC
    """
    mycursor.execute(sql, [int(bmid)])
    table = mycursor.fetchall()

    for row in table:
        print(",".join(str(column) for column in row))


def countCustomizedModel(*bmids):
    db = connection()
    mycursor = db.cursor()

    bmid_list = tuple(int(x) for x in bmids)
    placeholders = ",".join(["%s"] * len(bmid_list))

    sql = f"""
        SELECT b.bmid, b.description, COUNT(c.mid) AS customizedModelCount
        FROM BaseModel b
        LEFT JOIN CustomizedModel c ON b.bmid = c.bmid
        WHERE b.bmid IN ({placeholders})
        GROUP BY b.bmid, b.description
        ORDER BY b.bmid ASC
    """

    mycursor.execute(sql, bmid_list)
    result = mycursor.fetchall()

    for row in result:
        print(",".join(str(x) for x in row))
        
def topNDurationConfig(uid, N):
    db = connection()
    mycursor = db.cursor()

    sql = """
        SELECT c.client_uid, c.cid, c.labels, c.content, mc.duration
        FROM Configuration c
        JOIN ModelConfigurations mc ON c.cid = mc.cid
        WHERE c.client_uid = %s
        ORDER BY mc.duration DESC
        LIMIT %s
    """

    mycursor.execute(sql, (int(uid), int(N)))
    result = mycursor.fetchall()

    for row in result:
        print(",".join(str(x) for x in row))
        
def listBaseModelKeyWord(keyword):
    db = connection()
    mycursor = db.cursor()

    sql = """
        SELECT DISTINCT b.bmid, i.sid, i.provider, l.domain
        FROM BaseModel b
        JOIN ModelServices ms ON b.bmid = ms.bmid
        JOIN InternetService i ON ms.sid = i.sid
        JOIN LLMService l ON l.sid = i.sid
        WHERE l.domain LIKE %s
        ORDER BY b.bmid ASC
        LIMIT 5
    """

    like_pattern = "%" + keyword + "%"

    mycursor.execute(sql, (like_pattern,))
    result = mycursor.fetchall()

    for row in result:
        print(",".join(str(x) for x in row))

def printNL2SQLresult():
    with open('results.csv', 'r') as file:
        reader = csv.reader(file)
        for lines in reader:
            print(lines)

def main():
    # sys.argv
    # [0] - project.py 
    # [1] - (command)
    # [2] - Other Parameters
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
            case "countCustomizedModel":
                countCustomizedModel(*sys.argv[2:])
            case "topNDurationConfig":
                topNDurationConfig(sys.argv[2], sys.argv[3])
            case "listBaseModelKeyWord":
                listBaseModelKeyWord(sys.argv[2])
            case "printNL2SQLresult":
                printNL2SQLresult()
    
    except mysql.connector.ProgrammingError as exc:
        print("Error!", exc)


if __name__ == "__main__":
    main()
