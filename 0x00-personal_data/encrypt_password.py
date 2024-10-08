#!/usr/bin/env python3
"""encrypting passwords.
"""


import logging
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password string bytest.
    """
    # Salt and hash the password using the bcrypt package
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hash
    """
    # Try to match the hashed password with the given password
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    # If there is an exception in the process, log the error message
    except Exception as e:
        logging.error("Error in password validation: {}".format(e))
        return False
