from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

SQL_HOST = os.environ.get("SQL_HOST")
SQL_USER = os.environ.get("SQL_USER")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")
SQL_DATABASE = os.environ.get("SQL_DATABASE")

mysqldb = mysql.connector.connect(
    host=SQL_HOST,
    user=SQL_USER,
    password=SQL_PASSWORD,
    database=SQL_DATABASE
)

mysqlcursor = mysqldb.cursor()

@app.route("/")
@app.route("/healthz")
def health_check():
    return jsonify({"status": 200, "healthy": True})

@app.route("/create", methods=['POST'])
def create():
    request_data = request.get_json()
    values = []
    for data in request_data['data']:
        values.append((data['id'], data['data']))
    sql = "INSERT INTO demo_table (id, data) VALUES (%s, %s)"
    mysqlcursor.executemany(sql, values)
    mysqldb.commit()
    return jsonify({
        "added": mysqlcursor.rowcount
    })

@app.route("/update", methods=['PUT'])
def update():
    request_data = request.get_json()
    sql = "UPDATE demo_table SET data='" + str(request_data['data']) + "' WHERE id=" + str(request_data['id'])
    mysqlcursor.execute(sql)
    mysqldb.commit()
    return jsonify({
        "updated": mysqlcursor.rowcount
    })

@app.route("/read", methods=['GET'])
def read():
    sql = "SELECT * FROM demo_table"
    mysqlcursor.execute(sql)
    return_data = {"data": []}
    for x in mysqlcursor.fetchall():
        return_data['data'].append({
            "id": x[0],
            "data": x[1]
        })
    return jsonify(return_data)

@app.route("/delete", methods=['DELETE'])
def delete():
    request_data = request.get_json()
    sql = "DELETE FROM demo_table WHERE id=" + str(request_data['id'])
    mysqlcursor.execute(sql)
    mysqldb.commit()
    return jsonify({
        "deleted": mysqlcursor.rowcount
    })

def setup():
    mysqlcursor.execute("CREATE TABLE IF NOT EXISTS demo_table(id int, data varchar(50))")

if __name__=="__main__":
    setup()
    app.run(host='0.0.0.0')