from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.login_service import LoginService

app = FastAPI()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        PUBLIC_PATHS = {"/api/login", "/health"}
        if request.url.path in PUBLIC_PATHS:  # Allow public auth routes
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "missing authorization token"})  # Properly return 401

        
        token = auth_header.split("Bearer ")[1]
        try:
            LoginService.verify_token(token)
        except Exception as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})

        return await call_next(request)   
