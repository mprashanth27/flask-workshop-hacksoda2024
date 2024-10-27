#app.py for the server 
from flask import Flask, request, jsonify, render_template
from db import db
from config import Config
from routes import app as main


def create_app(): 
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #initialize the database
    db.init_app(app)
    
    #register the blueprint for the routes
    app.register_blueprint(main)
    
    #create the databse tables
    with app.app_context():
        db.create_all()
        
    return app

#run the flask app
if __name__ == "__main__":
    
    #create the app
    app = create_app()
    app.run(debug=True)

