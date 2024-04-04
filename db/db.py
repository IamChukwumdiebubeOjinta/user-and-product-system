import logging
import os
import json
from json.decoder import JSONDecodeError
from fastapi import HTTPException

user_db = []
file_path = "db/"

def connect_db(file):
    global user_db
    global file_path

    db_file = os.path.join(file_path, file)
    db_exists = os.path.exists(db_file)
    db_empty = os.path.isfile(db_file) and os.path.getsize(db_file) == 0

    if not db_exists or db_empty:
        with open(db_file, "w") as f:
            json.dump(user_db, f)
        print("--------------------------------")
        print("Database created successfully")
        print("--------------------------------")
    else:
        with open(db_file, "r") as f:
            user_db = json.load(f)
        print("--------------------------------")
        print("Database connected successfully")
        print("--------------------------------")

# db.py
def write_to_db(user_db, file):
    """
    Writes the user database to a file.

    Args:
        user_db (dict): The user database.
        file (str): The name of the file to write to.

    Returns:
        None
    """
    global file_path
    db_file = os.path.join(file_path, file)
    try:
        with open(db_file, "w") as f:
            json.dump(user_db, f, indent=4)
        logging.info("Data written to database successfully")
    except (FileNotFoundError, IOError) as e:
        logging.error(f"Error writing to file: {e}")


def read_from_db(file):
    global user_db
    global file_path

    db_file = os.path.join(file_path, file)
    try:
        with open(db_file, "r") as f:
            data = f.read()
            if not data:
                raise Exception("Null pointer reference: file is empty")
            user_db = json.loads(data)
        print(f"Loaded {len(user_db)} records from {db_file}")
        return user_db
    except (JSONDecodeError, Exception) as e:
        print(f"Error reading {db_file}: {e}")
        user_db = []
        return user_db
    except FileNotFoundError as e:
        print(f"File not found: {db_file}")
        connect_db(file)
        return []



