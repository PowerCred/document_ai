from google.cloud import storage
import aiohttp
from os import path, getenv
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from . import CommonLogger

class Gcs:
    def __init__(self):
        """
        Initializes the Gcs class by setting up the bucket name and credentials for Google Cloud Storage.

        Raises:
            EnvironmentError: If required environment variables are not set.
        """
        self.logger = CommonLogger.get_logger(__name__)
        self.__bucket_name = bucket_name if bool(bucket_name) else getenv('BUCKET')
        if not self.__bucket_name:
            raise EnvironmentError('Please specify google bucket name. You can do "export BUCKET=<YOUR_BUCKET_NAME>"')
        
        google_credentials = getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not google_credentials:
            raise EnvironmentError('Please set GOOGLE_APPLICATION_CREDENTIALS to authorize access to GCS bucket')

    async def download_file(self, filepath: str, local_path: str):
        """
        Asynchronously downloads a file from Google Cloud Storage (GCS).

        Args:
            filepath (str): The path of the file in the GCS bucket.
            output_path (str): The local path to store the downloaded file.

        Returns:
            tuple: A tuple containing a boolean status and the output filepath.

        Raises:
            google.cloud.exceptions.GoogleCloudError: If an error occurs during download from GCS.
            FileNotFoundError: If the specified blob does not exist in the bucket.
        """
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.__bucket_name)
            blob = bucket.blob(filepath)
            output_filepath = path.join(output_path, path.basename(filepath))

            if blob.exists():
                # Using ThreadPoolExecutor to perform blocking IO operations asynchronously
                with ThreadPoolExecutor() as pool:
                    await asyncio.get_event_loop().run_in_executor(pool, blob.download_to_filename, output_filepath)
                return True, output_filepath 
            else:
                raise FileNotFoundError(f'Blob {filepath} not found in bucket {self.__bucket_name}')

        except storage.exceptions.GoogleCloudError as e:
            self.logger.error(f"Error downloading from GCS: {e}")
            raise e