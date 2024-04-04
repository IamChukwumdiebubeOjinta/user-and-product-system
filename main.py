import uvicorn
from fastapi import FastAPI
from user import user_routes
from db.db import connect_db
from fastapi.openapi.utils import get_openapi

# from config import custom_openapi

app = FastAPI()
users_file = "users.json"

if user_routes:
    connect_db(users_file)

@app.get('/', tags=["Root"])
async def home():
    return {"message": "Hello, world!"}

"""
Users Registration API
"""
app.include_router(user_routes.router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Users Registration & Products API",
        version="2.5.0",
        summary="This is a simple user auth and product app",
        description="",
        routes=app.routes,
        
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

custom_openapi()

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)