import jwt
import datetime
from django.conf import settings
from api.models import User  # Import your custom User model

def generate_jwt_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + settings.JWT_CONFIG["ACCESS_TOKEN_EXPIRY"],
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_CONFIG["ALGORITHM"])
    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_CONFIG["ALGORITHM"]])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
