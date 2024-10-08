# backend/app.py

from flask import Flask
from flask_cors import CORS
from routes import overlay_routes
from flasgger import Swagger
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
Swagger(app)  # Initialize Swagger for API documentation

# Register Blueprints
app.register_blueprint(overlay_routes, url_prefix='/api/overlays')

@app.route('/')
def home():
    return "Backend is running!"

if __name__ == '__main__':
    app.run(debug=True)
