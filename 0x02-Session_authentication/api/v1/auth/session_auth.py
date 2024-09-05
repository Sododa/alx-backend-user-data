#!/usr/bin/env python3
"""r the API.
"""


from uuid import uuid4

from models.user import User

from .auth import Auth


class SessionAuth(Auth):
    """Session authentication class that inherits
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id.
        """
        # If user_id is not None and is of type str
        if type(user_id) is str:
            # s uuid4() function
            session_id = str(uuid4())
            # ID in the dictionary,
            # user_id_by_session_id,
            # the session
            self.user_id_by_session_id[session_id] = user_id
            # Return the session ID
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID for a give
        """
        # If session_id is not None or is a string
        if type(session_id) is str:
            # Return the value (user ID) for the key session_id in dictionary
            # user_id_by_session_id
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Returns a User instance
        """
        # Retrieve the value of the _my_session_id cookie from the request
        session_id = self.session_cookie(request)
        # Look up the corresponding User ID based on the session_id
        user_id = self.user_id_for_session_id(session_id)
        # Retrieve the User instance from the database based on the user_id
        user = User.get(user_id)
        # Return
        return user

    def destroy_session(self, request=None):
        """Delete the user session (log out the user)
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        # If the request
        # If the request
        # If the Session
        # return
        if (request is None or session_id is None) or user_id is None:
            return False
        # Otherwise
        # key
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        # Return
        return True
