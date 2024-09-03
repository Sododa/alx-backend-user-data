#!/usr/bin/env python3
"""basic authentication
"""
import base64
import binascii
from typing import Tuple, TypeVar

from models.user import User

from .auth import Auth


class BasicAuth(Auth):
    """Basic authenticion
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization
        """
        # Return None if authorization_header is None or if
        # authorization_header is not a string
        if authorization_header is None or not \
                isinstance(authorization_header, str):
            return None
        # Return None if authorization_header doesn’t start by Basic (with a
        # space at the end)
        if not authorization_header.startswith("Basic "):
            return None
        # Otherwise, return the value after Basic (after the space)
        return authorization_header.split("Basic ")[1].strip()

        # ALTERNATIVE SOLution

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the Base64 string `base64_authorization_header
        """
        # Return None
        if base64_authorization_header is None:
            return None
        # Return None
        if not isinstance(base64_authorization_header, str):
            return None
        # Return None
        try:
            decoded = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            # Return the decoded value as UTF8 string
            return decoded.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_header: str) -> Tuple[str, str]:
        """Extract the user email and password from the decoded header string..
        """
        # Return None, None if decoded_header is None or
        # not a string
        if decoded_header is None or not isinstance(decoded_header, str):
            return None, None
        # Attemp
        try:
            email, password = decoded_header.split(':', 1)
        except ValueError:
            return None, None
        # Return
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on the email and password.
        """
        # Return None if user_email or user_pwd is None or not a string
        if not all(map(lambda x: isinstance(x, str), (user_email, user_pwd))):
            return None
        try:
            # Search for the user in the database
            user = User.search(attributes={'email': user_email})
        except Exception:
            return None
        # Return None if there is no user in the database with the given email
        if not user:
            return None
        # Gethefirstuserfromthesearchresults
        user = user[0]
        # ReturnNonefe password is invalid
        if not user.is_valid_password(user_pwd):
            return None
        # Retu user instance
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ReArgs:
            request (:obj:`Request`, optional): The request object. Defaults
            ance based on the request.
        """
        # Get the authorization
        auth_header = self.authorization_header(request)
        #the Base64 encoded string from th
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        # the Base64 g
        dec_header = self.decode_base64_authorization_header(b64_auth_header)
        # user email and password fromg
        user_email, user_pwd = self.extract_user_credentials(dec_header)
        # Re based on the used
        return self.user_object_from_credentials(user_email, user_pwd)
