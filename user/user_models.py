import re
import bcrypt
from db.db import read_from_db
from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

# Define the regex pattern as a constant
PASSWORD_PATTERN = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
# Defining the users file
users_file = "users.json"


class UserModel(BaseModel):
    id: str
    firstname: str = Field(max_length=20, min_length=3, description="User's first name")
    lastname: str = Field(max_length=20, min_length=3, description="User's last name")
    email: EmailStr = Field(description="User's email address")
    password: str = Field(
        description="Please enter a password that meets our security criteria",
        min_length=8,
    )
    
    @field_validator("password")
    def validate_password(cls, v):
        # Validates the password value using a regular expression pattern.
        if not re.match(PASSWORD_PATTERN, v):
            raise ValueError("Password does not meet security criteria.")
        return v
    
class UpdateUser(BaseModel):
    firstname: Optional[str] = Field(None, max_length=20, min_length=3, description="User's first name")
    lastname: Optional[str] = Field(None, max_length=20, min_length=3, description="User's last name")
    
class CreateNewUser:
    
    @classmethod
    def create_user(cls, user: UserModel) -> UserModel:
        """
        Creates a new user with the provided user data.

        :param user: The user data to create the user.
        :type user: UserModel
        :return: The newly created user.
        :return_type: UserModel
        """
        # Check if user with the same email already exists
        existing_user = cls._get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="User with the same email already exists")

        try:
            # Hashing the password
            encoded_password = user.password.encode()
            salt = bcrypt.gensalt(10)
            hashed_password = bcrypt.hashpw(encoded_password, salt)
        except Exception as e:
            # Handle the exception
            print(f"Error occurred during password hashing: {e}")
            hashed_password = None
            print(f"hashed_password: {hashed_password}")
  
        return {
            "id": cls._get_next_id(),
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "password": hashed_password.decode(),
        }

    @classmethod
    def _get_next_id(cls) -> int:
        """Get the next available id by reading the latest id from the DB"""
        users = read_from_db(users_file)
        latest_id = max(user["id"] for user in users) if users else 0
        return latest_id + 1

    @classmethod
    def _get_user_by_email(cls, email: str) -> UserModel:
        """Get user by email from the DB"""
        users = read_from_db(users_file)
        for user in users:
            if email == user["email"]:
                return user
        return None
