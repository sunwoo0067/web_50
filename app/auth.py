import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from app.models import User

SECRET_KEY = 'your_jwt_secret_key'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': '토큰이 존재하지 않습니다.'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': '토큰이 유효하지 않습니다.'}), 401
        return f(current_user, *args, **kwargs)
    return decorated 