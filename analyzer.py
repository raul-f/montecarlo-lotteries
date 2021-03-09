import mysql.connector as mysql

def main():
    db = mysql.connect(
        host = 'localhost',
        user = 'root',
        password = '04B438u?y',
        database = 'simulador_loterias'
    )
    cursor = db.cursor()

    cursor.execute('SELECT * FROM Runs')

    result = cursor.fetchall()

    print(result)

main()
