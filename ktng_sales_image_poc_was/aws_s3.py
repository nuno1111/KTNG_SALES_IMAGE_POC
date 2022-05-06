import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_s3_image(file_name, bucket, object_name):

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_s3_image(bucket, key):

    s3_client = boto3.client('s3')
    file = s3_client.get_object(Bucket=bucket, Key=key)

    return file


# def upload_s3_image(bucket, key, image, content_type):
#     s3_client = boto3.client('s3')
#     response = s3_client.put_object(
#         Bucket=bucket,
#         Body=image,
#         Key=key,
#         ContentType=content_type)
#     return response
