from flask_mysqldb import MySQL

mysql = MySQL()
#Initializes the configuration of the database in a mysql variable
def init_db(app):
    app.config["MYSQL_HOST"] = app.config["MYSQL_HOST"]
    app.config["MYSQL_USER"] = app.config["MYSQL_USER"]
    app.config["MYSQL_PASSWORD"] = app.config["MYSQL_PASSWORD"]
    app.config["MYSQL_DB"] = app.config["MYSQL_DB"]
    
    mysql.init_app(app)
    
#It returns the connection of the database
def get_db_connection():
    return mysql.connection
#It returns the cursor
def get_cursor():
    conn = get_db_connection()
    return conn.cursor()