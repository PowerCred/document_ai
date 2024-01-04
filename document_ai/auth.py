from .utils import Manager, CommonLogger
import logging
import aiohttp


class Auth(Manager):
    def __init__(self, secret: str):
        super().__init__()  # Call the constructor of the base class if needed
        self.__secret = secret
        self.logger = CommonLogger.get_logger(__name__)

    async def get_session_token(self, user_id: str, redirect_url: str = None):
        """
        Asynchronously requests a session token for a given user.

        Args:
            user_id (str): The user's ID for whom the token is requested.
            redirect_url (str, optional): A URL to redirect after token generation. Defaults to None.

        Returns:
            Response or error message based on the outcome of the request.

        Raises:
            Specific exceptions related to request failures for better error handling.
        """
        try:
            req_body = {
                'user_id': user_id
            }
            params = {'secret': self.__secret}
            if redirect_url:
                params['redirect_url'] = redirect_url

            auth_url = f'{self.url}/auth/token'
            response, status = await self.url_requests(url=auth_url, params=params, json=req_body, method='post')

            if status == 200:
                return response
            else:
                self.logger.error(f"Error in get_session_token: {response}")
                return f'Something went wrong: {response}'

        except aiohttp.ClientError as e:
            self.logger.error(f"Client Error in get_session_token: {e}")
            raise
        except aiohttp.ClientConnectionError as e:
            self.logger.error(f"Connection Error in get_session_token: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected Error in get_session_token: {e}")
            raise
