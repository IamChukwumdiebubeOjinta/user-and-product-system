"""
    This controller handles user registration operations.
    Endpoints include:
        GET /users: Retrieve all users.
        GET /users/{user_id}: Retrieve a specific user by ID.
        POST /users: Create a new user.
"""
import os
import bcrypt
import json
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .user_models import UserModel, CreateNewUser, UpdateUser
from db.db import read_from_db, write_to_db

file = "users.json"

def get_users():
    users = read_from_db(file)
    return JSONResponse(status_code=201, content=users)

def get_user(id: int):
    """
    Get the user by the given id.

    Parameters:
        id (int): The id of the user.

    Returns:
        dict: A dictionary with a message indicating that the user is being retrieved.
    """
    users = read_from_db(file)
    for user in users:
        if id == user["id"]:
            return {"status_code": 201, "data": user}
    return None

def create_user(user):
    """
    A function that creates a new user in the database and returns the user data.
    
    Parameters:
    user (dict): A dictionary containing the user information.
    
    Returns:
    dict: A dictionary with the status code and the new user data.
    """
    users = read_from_db(file)
    
    try:
        init_user_class = CreateNewUser()
        new_user = init_user_class.create_user(user)
        
        # add_user_to_db: list = users.append(new_user.dict())
        # users[new_user.id] = new_user.dict()
        users.append(new_user)
        write_to_db(users, file) 
        user_data = {
        "status_code": 201,
        "data": new_user, 
        } 
        return user_data
    except HTTPException as e:
        return HTTPException(status_code=500, detail=str(e))
    
def update_user(id: int, user: UpdateUser):
    """
    Update a user's information in the database based on the provided ID and user object.

    Parameters:
    - id (int): The ID of the user to update.
    - user (UpdateUser): The object containing the updated user information.

    Returns:
    - dict: If the user was successfully updated, return the updated user's information.
    - dict: If the user was not found, return a message indicating the user was not updated.
    """
    users = read_from_db(file)
    for i in range(len(users)):
        if users[i]["id"] == id:
            users[i]["firstname"] = user.firstname or users[i]["firstname"]
            users[i]["lastname"] = user.lastname or users[i]["lastname"]
            write_to_db(users, file)
            return users[i]
    return {"msg": "user updated successfully"}

def delete_user(id: int):
    """
    A function to delete a user from the database given the user's ID.
    Parameter:
        id: int - the ID of the user to be deleted.
    Returns:
        dict - a message indicating if the user was deleted successfully or the updated list of users.
    """
    users = read_from_db(file)
    for i in range(len(users)):
        if users[i]["id"] == id:
            print(id)
            del users[i]
            write_to_db(users, file)
            return users
    return {"msg": "user deleted successfully"}