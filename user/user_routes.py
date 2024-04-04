from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from .user_controllers import create_user, get_user, get_users, update_user, delete_user
from .user_models import UserModel, UpdateUser
from fastapi.openapi.utils import get_openapi


router = APIRouter(prefix="/api/v1", tags=["Users"])

@router.get("/users", response_model=list[UserModel])
def get_users_route():
    """Get all users."""
    return get_users()

@router.get("/user/{id}")
def get_user_route(id: int):
    """Get a user by ID."""
    user = get_user(id)
    if user is None:
        return HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create_user")
def create_user_route(user: UserModel):
    """Create a new user."""
    _user = create_user(user)
    if _user is None:
        return HTTPException(status_code=409, detail="User not found")
    return _user

@router.patch("/users/{id}")
def update_user_route(id: int, user: UpdateUser):
    """Update a user by ID."""
    _user = update_user(id, user)
    if _user is None:
        return HTTPException(status_code=404, detail="User not found")
    return _user

@router.delete("/users/{id}")
def delete_user_route(id: int):
    """Delete a user by ID"""
    deleted_user = delete_user(id)
    if not deleted_user is None:
        return HTTPException(status_code=404, detail="User not found")
    return deleted_user