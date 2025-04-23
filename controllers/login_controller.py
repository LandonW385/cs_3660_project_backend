import datetime
import hashlib
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from schemas.login_schema import LoginRequest, LoginResponse, VerifyLoginRequest
from services.login_service import LoginService


router = APIRouter(prefix="/api/login", tags=["Authentication"])

@router.post("", response_model=LoginResponse)
async def login(login: LoginRequest):
    """
    Authenticate the user and return a JWT token along with the username.
    """
    try:
        token = LoginService.get_login_token(login.username, login.password)
        return {
            "success": True,
            "jwt_token": token,
            "username": login.username  # Include the username in the response
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@router.post("/verify", response_model=LoginResponse)
async def verify(verify_request: VerifyLoginRequest):
    try:
        _ = LoginService.verify_token(verify_request.jwt_token)
        return LoginResponse(success=True, jwt_token=verify_request.jwt_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Define a Pydantic model for the signup request
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(user: SignupRequest):
    """
    Register a new user.
    """
    try:
        # Load existing users
        with open("./db/users.json", "r") as file:
            data = json.load(file)

        # Check if the email is already registered
        for existing_user in data["users"]:
            if existing_user["username"] == user.email:
                raise HTTPException(status_code=400, detail="Email is already registered")

        # Hash the password
        password_hash = hashlib.sha256(user.password.encode()).hexdigest()

        # Add the new user
        new_user = {
            "username": user.email,
            "name": user.name,
            "password_hash": password_hash,
            "coins": 100  # Default coin balance for new users
        }
        data["users"].append(new_user)

        # Save the updated users list
        with open("./db/users.json", "w") as file:
            json.dump(data, file, indent=4)

        return {"message": "User registered successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="User database not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

