#!/usr/bin/env python3
"""
Mentication
"""
from typing import List, TypeVar

from flask import request


class Auth():
    """Template system implemented in this app.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This function takes a path and a list of excluded paths as arguments
        and returns a boolean val.
        """
        # If path is None, return True
        if not path:
            return True
        # If _paths is None or empty, return True
        if not excluded_paths:
            return True
        # Remove theg slash from the path
        path = path.rstrip("/")
        # Check if path is is and return False if path is
        # ind_paths
        # Loop d paths
        for excluded_path in excluded_paths:
            # Check if givenexcluded path, with * at the end
            if excluded_path.endswith("*") and \
                    path.startswith(excluded_path[:-1]):
                # Return False excluded path with * at end
                return False
            # Check if the given excluded path
            elif path == excluded_path.rstrip("/"):
                # Return Fath
                return False
        # If
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the value of the Authorization header from the request
        """
        # If request is None, return None
        # If request doesn’t contain the header key Authorization, return None
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """This function takes a request object as an optional argument.
        """
        return None
