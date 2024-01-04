import aiohttp
import logging
from os import getenv, makedirs, path
import mimetypes
from tempfile import gettempdir
from aiohttp import ClientError, ClientConnectionError, ContentTypeError

logger = logging.getLogger(__name__)

class Manager:
    def __init__(self, apikey: str = None, enviromnent: str = 'DEV'):
        self.__apikey = apikey if bool(apikey) else getenv('APIKEY')
        urls = {
            'dev': 'https://mock.powercred.io',
            'prod': 'https://dev.powercred.io'
        }
        if enviromnent not in ['DEV', 'PROD']:
            raise AttributeError(f'Invalid environment {enviromnent} specified; please enter DEV or PROD')

        self.url = urls[enviromnent.lower()]
        if not self.__apikey:
            raise AttributeError('No API key found. Please set APIKEY environment variable!')
        
    async def url_requests(self, url: str, json: dict = None, params: dict = None, headers: dict = None, method: str = 'get', **kwargs) -> dict:
        """
        Asynchronously makes HTTP requests using aiohttp and handles various types of responses.

        This function supports both JSON and non-JSON responses. It includes exception handling
        for common network and HTTP errors, and uses logging for error reporting and informational messages.

        Args:
            url (str): The URL to which the HTTP request is to be made.
            json (dict, optional): A JSON payload to send in the request body. Defaults to None.
            params (dict, optional): Query parameters to append to the URL. Defaults to None.
            headers (dict, optional): HTTP headers to send with the request. Defaults to None.
            method (str, optional): HTTP method to use (e.g., 'get', 'post', 'put'). Defaults to 'get'.
            **kwargs: Additional keyword arguments that aiohttp.ClientSession can accept.

        Returns:
            tuple: A tuple containing the response data and status code.
                   The response data is either a dict (for JSON responses) or a string (for others).

        Raises:
            ContentTypeError: If the response content type is not as expected.
            ClientError: For client-side errors like invalid URL, payload, etc.
            ClientConnectionError: For errors related to network connections.
            Exception: For any other unforeseen errors.
        """
        try:
            connector = aiohttp.TCPConnector(limit=150)
            logger.info("url requests called")
            async with aiohttp.ClientSession(headers=headers, connector=connector) as session, connector:
                request_method = getattr(session, method)
                if params:
                    params.update({
                        'apikey': self.__apikey
                    })
                if not json:
                    response = await request_method(url, params=params, **kwargs)
                else:
                    response = await request_method(url, params=params, json=json, **kwargs)

                status = response.status
                if response.headers['Content-Type'] == 'application/json':
                    data = await response.json()
                else:
                    data = await response.text()

                logger.info(f"Response Data: {data.keys()} Status: {status}")
                return data, status

        except ContentTypeError as e:
            logger.error(f"Content Type Error: {e}")
            return str(e), status
        except ClientError as e:
            logger.error(f"Client Error: {e}")
            return str(e), status
        except ClientConnectionError as e:
            logger.error(f"Connection Error: {e}")
            return str(e), status
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            return str(e), 500  # 500 is a general code for server error

    async def get_temp_dir(self, id: str):
        """
        Asynchronously creates a temporary directory for a given ID and returns its path.

        Args:
            id (str): The unique identifier for the temporary directory.

        Returns:
            str: The path to the created temporary directory.

        Raises:
            OSError: If there's an error in creating the directory.
        """
        try:
            folderpath = path.join(gettempdir(), id)
            # Creates the directory; does nothing if the directory already exists
            makedirs(folderpath, exist_ok=True)
            return folderpath
        except OSError as e:
            # Log the error or handle it as needed
            raise e

    def get_mime_type_with_mimetypes(self, filename):
        mime_type, encoding = mimetypes.guess_type(filename)
        return mime_type