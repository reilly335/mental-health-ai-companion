# app.py

from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from datetime import timedelta
import os

app = Flask(__name__)

# Configuration
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Database setup
client = MongoClient('mongodb://mongo-service:27017/')
db = client['mh_ai_db']
users_collection = db['users']

# Routes

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "SecurePassword123"
    }
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    if users_collection.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user_data = {
        'email': email,
        'password': hashed_password,
        'role': 'user',  # Default role can be 'user' or 'professional'
        # Additional fields can be added here
    }

    users_collection.insert_one(user_data)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and return a JWT access token.
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "SecurePassword123"
    }
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Create JWT access token
    access_token = create_access_token(identity={'email': user['email'], 'role': user['role']})
    return jsonify({'access_token': access_token}), 200

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """
    Get the current user's information.
    """
    current_user = get_jwt_identity()
    user = users_collection.find_one({'email': current_user['email']}, {'_id': 0, 'password': 0})
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Handle user logout if token revocation is implemented.
    """
    # Token revocation logic can be added here
    return jsonify({'message': 'User logged out successfully'}), 200

if __name__ == '__main__':
    # Ensure the secret key is set securely in a production environment
    app.run(host='0.0.0.0', port=5000)
