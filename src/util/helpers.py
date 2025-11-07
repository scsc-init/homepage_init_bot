import hashlib
import hmac

from src.core import get_settings


def generate_user_hash(email: str) -> str:
    secret = get_settings().api_secret.encode()
    msg = email.lower().encode()
    return hmac.new(secret, msg, hashlib.sha256).hexdigest()
