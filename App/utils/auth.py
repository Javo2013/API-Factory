from functools import wraps
from flask import request, jsonify, current_app, g
from jose import jwt, JWTError

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Grab token from Authorization header
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            parts = auth.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            # Store mechanic_id so routes can use it
            g.mechanic_id = payload["sub"]
            print("TOKEN MECHANIC ID:", g.mechanic_id)

        except JWTError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
