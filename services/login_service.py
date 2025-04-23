from fastapi import HTTPException
import jwt # pip install PyJWT
import datetime
import hashlib

from repositories.user_repository import UserRepository

SECRET_KEY = "your_secret_key_your_secret_key_your_secret_key_your_secret_key"
ALGORITHM = "HS256"

class LoginService:
    @staticmethod
    def get_login_token(username: str, password: str) -> str:
        #get user account by username from login repo
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise Exception("User not found")

        #check the creds match
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if user.password_hash != hashed_password:
            raise Exception("Invalid credentials")

        #create jwt with secret key
        user_payload = {
            "username": user.username,
            "name": user.name
        }

        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        token_payload = {
            "sub": user.username,
            "exp": expiration_time,
            "user": user_payload
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

        return token

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            # Decode the token using the secret key and algorithm
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
