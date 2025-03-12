from flask import Flask
from models import init_db
from routes import main_bp
from config import Config
#Initializes the flask as main
app = Flask(__name__)
#It configures the database with the object config
app.config.from_object(Config)
#It initialize the database
init_db(app)
#It registers the endpoints of the blueprint created
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)