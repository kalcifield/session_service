import hashlib
from base64 import b64encode
from os import urandom


class SessionGenerator:

    @staticmethod
    def generate_session_id(user_id):
        random_bytes = urandom(32)
        token = b64encode(random_bytes).decode('utf-8')
        user_name = user_id.rsplit('@', 1)[0]  # split email@csodafone.com at '@' sign and get first part
        hashed_user_name = hashlib.md5(user_name.encode()).hexdigest()
        return str(token + hashed_user_name)
