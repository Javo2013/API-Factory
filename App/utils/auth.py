from functools import wraps
from flask import request, jsonify, current_app, g
from jose import jwt, JWTError, ExpiredSignatureError


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split()

            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        # Decode Token
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            # Store mechanic_id for current request
            g.mechanic_id = payload["sub"]

        except ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except JWTError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated