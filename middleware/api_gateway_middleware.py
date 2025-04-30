from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings

app = FastAPI()

class ApiGatewayMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # all calls need api token, this is how we'll prevent random calls to our api
        # not coming from aws api gateway
        api_token_header = request.headers.get("x-api-token")
        if not api_token_header or api_token_header != settings.api_gateway_token:
            # if not present or not matching, return 403 forbidden
            return JSONResponse(status_code=403,content={"message": "Forbidden"})
        
        return await call_next(request)