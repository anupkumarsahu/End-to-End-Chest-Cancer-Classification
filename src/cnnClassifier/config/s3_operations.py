import os
import sys

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket

from io import StringIO
from typing import List, Union

from cnnClassifier.exception import CNNException
from src.cnnClassifier.constants import *
from src.cnnClassifier.logger import logger


class S3Operation:
    s3_client = None
    s3_resource = None

    def __init__(self):
        if S3Operation.s3_resource == None or S3Operation.s3_client == None:
            __access_key_id = os.getenv(
                AWS_ACCESS_KEY_ID_ENV_KEY,
            )
            __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

            if __access_key_id is None:
                raise Exception(
                    f"Environment variable: {AWS_ACCESS_KEY_ID_ENV_KEY} is not set"
                )

            if __secret_access_key is None:
                raise Exception(
                    f"Environment variable: {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set"
                )

            S3Operation.s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=REGION_NAME,
            )

            S3Operation.s3_client = boto3.client(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=REGION_NAME,
            )

            self.s3_resource = S3Operation.s3_resource
            self.s3_client = S3Operation.s3_client

    @staticmethod
    def read_object(
        object_name: str, decode: bool = True, make_readable: bool = False
    ) -> Union[StringIO, str]:
        """_summary_

        Args:
            object_name (str): _description_
            decode (bool, optional): _description_. Defaults to True.
            make_readable (bool, optional): _description_. Defaults to False.

        Raises:
            CNNException: _description_

        Returns:
            Union[StringIO, str]: _description_
        """        
        logger.info("Enter the read_object method of S3Operations class")

        try:
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )
            def conv_func(): return StringIO(func()) if make_readable is True else func()

            logger.info(
                f"Exited the read_object method of S3Operations class")

            return conv_func()
        except Exception as e:
            raise CNNException(e, sys) from e
        
    def get_bucket(self, bucket_name: str) -> Bucket:
        """

        :param bucket_name: provide bucket name
        :return: bucket object
        """
        logger.info(f"Entered the get_bucket method of S3Operations class")
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logger.info(f"Exited the get_bucket method of S3Operations class")
            return bucket
        except Exception as e:
            raise CNNException(e, sys) from e

    def get_file_object(
        self, filename: str, bucket_name: str
    ) -> Union[List[object], object]:
        """_summary_

        Args:
            filename (str): _description_
            bucket_name (str): _description_

        Raises:
            CNNException: _description_

        Returns:
            Union[List[object], object]: _description_
        """        
        logger.info(
            "Entered the get_file_object method of S3Operations class")

        try:
            bucket = self.get_bucket(bucket_name)
            lst_objs = [
                object for object in bucket.objects.filter(Prefix=filename)]

            def func(x): return x[0] if len(x) == 1 else x
            file_objs = func(lst_objs)

            logger.info(
                "Exited the get_file_object method of S3Operations class")
            return file_objs

        except Exception as e:
            raise CNNException(e, sys) from e

    def load_model(
        self, model_name: str, bucket_name: str, model_dir: str = None
    ) -> object:
        """_summary_

        Args:
            model_name (str): _description_
            bucket_name (str): _description_
            model_dir (str, optional): _description_. Defaults to None.

        Raises:
            CNNException: _description_

        Returns:
            object: _description_
        """        
        logger.info("Entered the load_model method of S3Operations class")

        try:
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )

            model_file = func()

            f_obj = self.get_file_object(model_file, bucket_name)

            model_obj = self.read_object(f_obj, decode=False)

            return model_obj
            logger.info("Exited the load_model method of S3Operations class")

        except Exception as e:
            raise CNNException(e, sys) from e

    def create_folder(self, bucket_name: str, folder_name: str) -> None:
        """_summary_

        Args:
            bucket_name (str): _description_
            folder_name (str): _description_
        """
        logger.info(f"Entered the create_folder method of S3Operations class")
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"

                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            else:
                pass

            logger.info(f"Exited the create_folder method of S3Operations class")

    def upload_file(
            self,
            from_filename: str,
            to_filename: str,
            bucket_name: str,
            remove: bool = True,
    ):
        """_summary_

        Args:
            from_filename (str): _description_
            to_filename (str): _description_
            bucket_name (str): _description_
            remove (bool, optional): _description_. Defaults to True.

        Raises:
            CNNException: _description_
        """
        logger.info(f"Entered the upload_file method of S3Operations class")
        try:
            logger.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )
            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )

            logger.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove is True:
                os.remove(from_filename)

                logger.info(f"Remove is set to {remove}, deleted the file")

            else:
                logger.info(f"Remove is set to {remove}, not deleted the file")

            logger.info("Exited the upload_file method of S3Operations class")
        except Exception as e:
            raise CNNException(e, sys) from e

    def read_data_from_s3(self, filename: str, bucket_name: str, output_filename: str):
        """_summary_

        Args:
            filename (str): _description_
            bucket_name (str): _description_
            output_filename (str): _description_

        Raises:
            CNNException: _description_

        Returns:
            _type_: _description_
        """
        try:
            bucket = self.get_bucket(bucket_name)

            obj = bucket.download_file(Key=filename, Filename=output_filename)

            return output_filename
        except Exception as e:
            raise CNNException(e, sys) from e
