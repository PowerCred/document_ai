import aiohttp
import logging
import asyncio
import aiofiles
from os import path

from . import CommonLogger


class URL:

    def __init__(self):
        self.logger = CommonLogger.get_logger(__name__)


    async def download_file(self, url: str, local_path: str):
        """
        Asynchronously downloads a file from a given URL.

        Args:
            url (str): The URL of the file to download.
            local_path (str): The local path to save the downloaded file.

        Raises:
            aiohttp.ClientError: If an error occurs during the HTTP request.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content_disposition = response.headers.get('Content-Disposition')
                        if content_disposition:
                            # Extract filename from Content-Disposition
                            filename = content_disposition.split(';')[1].split('=')[1].strip('\"')
                        else:
                            # If there's no Content-Disposition, use the URL to guess the filename
                            filename = url.split('/')[-1]
                        output_filepath = path.join(local_path, path.basename(filename))
                        # Using aiofiles to write the file asynchronously
                        async with aiofiles.open(output_filepath, 'wb') as file:
                            await file.write(await response.read())
                        self.logger.info(f"File downloaded successfully from URL: {url}")
                        return True, output_filepath
                    else:
                        self.logger.error(f"Failed to download file from URL: {url}, Status Code: {response.status}")
                        response.raise_for_status()
                        return False, f"Failed to download file from URL: {url}, Status Code: {response.status}"
        except Exception as e:
            self.logger.error(f"Error downloading from URL: {e}")
            raise
