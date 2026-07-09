from functools import wraps
from flask import request, jsonify, current_app
from jose import jwt, JWTError

def encode_token(customer_id):
    payload = {
        "customer_id": customer_id,
        "role": "customer"
    }
    
    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    
    return token

def encode_mechanic_token(mechanic_id):
    payload = {
        "mechanic_id": mechanic_id,
        "role": "mechanic"
    }
    
    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer"):
            return jsonify({"error": "Token is missing"}), 401
        
        token = auth_header.split(" ")[1]
        
        try: 
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            
            customer_id = payload.get("customer_id")
            
            if not customer_id:
                return jsonify({"error": "Invalid customer token"}), 401
        
        except JWTError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(customer_id, *args, **kwargs)
    
    return decorated

def mechanic_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token is missing"}), 401
        
        token = auth_header.split(" ")[1]
        
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            
            mechanic_id = payload.get("mechanic_id")
            role = payload.get("role")
            
            if not mechanic_id or role != "mechanic":
                return jsonify({"error": "Invalid mechanic token"}), 401
            
        except JWTError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(mechanic_id, *args, **kwargs)
    
    return decorated