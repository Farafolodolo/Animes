import os
#This is for adding all the configuration of the database and the secret key
class Config:
    #It detects if the environment has a secret key, if not, it will put a default secret key
    SECRET_KEY = os.getenv("SECRET_KEY", "IctionFRIt")
    
    #all the configuration for the database
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "animes"