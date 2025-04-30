from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from fastapi.middleware.cors import CORSMiddleware

from config import settings
from controllers import login_controller, store_controller, spotify_controller, music_queue_controller
from middleware.api_gateway_middleware import ApiGatewayMiddleware
from middleware.auth_middleware import AuthMiddleware

app = FastAPI(title="TuneGether Backend", version="1.0.0")

app.add_middleware(AuthMiddleware)

if settings.app_env == "local":
    app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.allow_origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
    )

if settings.app_env == "prod":
    app.add_middleware(ApiGatewayMiddleware)


app.include_router(login_controller.router)
app.include_router(store_controller.router)
app.include_router(spotify_controller.router)
app.include_router(music_queue_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TuneGether API"}

@app.get("/health")
def read_root():
    return {"message": "ok"}




def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="CS3660 Backend Project",
        routes=app.routes,
    )

    openapi_schema["openapi"] = "3.0.1"

    # Normalize paths to remove trailing slashes
    openapi_schema["paths"] = {
        path.rstrip("/") if path != "/" else path: data
        for path, data in openapi_schema["paths"].items() if path != ""
    }

    # Ensure all schemas have a "type" and remove unsupported constructs
    for schema_name, schema in openapi_schema["components"]["schemas"].items():
        if "properties" in schema:
            for field_name, field in schema["properties"].items():
                if "anyOf" in field:
                    field["type"] = "string"  # Replace 'anyOf' with a supported type
                    field["nullable"] = True
                    del field["anyOf"]

        # Add "type": "object" if missing
        if "type" not in schema:
            schema["type"] = "object"

    # Ensure all responses explicitly define a "type"
    for path, methods in openapi_schema["paths"].items():
        for method, data in methods.items():
            if "responses" in data:
                for status_code, response in data["responses"].items():
                    if "content" in response:
                        for content_type, content in response["content"].items():
                            if "schema" in content:
                                schema = content["schema"]
                                if "$ref" not in schema and "type" not in schema:
                                    schema["type"] = "object"  # Add "type" explicitly

    # Convert operationId to CamelCase for AWS compatibility
    for path, methods in openapi_schema["paths"].items():
        for method, data in methods.items():
            if "operationId" in data:
                data["operationId"] = "".join(
                    word.capitalize() for word in data["operationId"].split("_")
                )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi