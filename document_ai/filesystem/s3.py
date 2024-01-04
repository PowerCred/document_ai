import boto3
import logging
from os import path, getenv
from concurrent.futures import ThreadPoolExecutor
import asyncio

from . import CommonLogger

class S3:
    def __init__(self, bucket_name: str = None):
        """
        Initializes the S3 class with AWS credentials.

        Raises:
            EnvironmentError: If AWS credentials are not configured properly.
        """
        self.logger = CommonLogger.get_logger(__name__)
        self.__bucket_name = bucket_name if bool(bucket_name) else getenv('BUCKET')
        if not self.__bucket_name:
            raise EnvironmentError('Please specify S3 bucket name. You can do "export BUCKET=<YOUR_BUCKET_NAME>"')
        # Check if AWS credentials are available
        if not (getenv('AWS_ACCESS_KEY_ID') and getenv('AWS_SECRET_ACCESS_KEY')):
            raise EnvironmentError("AWS credentials not found. Please configure them.")

    async def download_file(self, filepath: str, local_path: str):
        """
        Asynchronously downloads a file from AWS S3.

        Args:
            bucket_name (str): The name of the S3 bucket.
            s3_key (str): The key of the file in the S3 bucket.
            local_path (str): The local path to save the downloaded file.

        Raises:
            boto3.exceptions.Boto3Error: If an error occurs during download from S3.
        """
        try:
            s3_client = boto3.client('s3')
            output_filepath = path.join(local_path, path.basename(filepath))
            # Using ThreadPoolExecutor to perform blocking IO operations asynchronously
            with ThreadPoolExecutor() as pool:
                await asyncio.get_event_loop().run_in_executor(
                    pool, 
                    s3_client.download_file, 
                    self.__bucket_name, 
                    filepath, 
                    output_filepath
                )
            self.logger.info(f"File downloaded successfully from S3: {s3_key}")
            return True, output_filepath 
        except Exception as e:
            self.logger.error(f"Error downloading from S3: {e}")
            raise e
