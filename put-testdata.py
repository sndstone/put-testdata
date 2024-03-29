import boto3
import concurrent.futures
import os
import uuid
from prettytable import PrettyTable
import json
import logging
from threading import Thread
from queue import Queue
import argparse

# Setup logging
LOG_FILENAME = 's3_upload.log'
file_logger = logging.getLogger('file_logger')

file_handler = logging.FileHandler(LOG_FILENAME)
file_logger.addHandler(file_handler)

# Function to read credentials from JSON file
def read_credentials_from_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            credentials = json.load(json_file)
            return credentials
    except Exception as e:
        file_logger.error(f'Error reading JSON: {e}')
        return None

# Logging function
def log_thread(q):
    while True:
        message = q.get()
        if message is None:
            break
        file_logger.log(logging.INFO, message)
        if "Put object" in message:
            print(message)
        q.task_done()

# Function to get integer input
def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

# Argument parser
parser = argparse.ArgumentParser(description="Upload files to S3")
parser.add_argument("--import_json", help="Path to JSON file for configuration", default=None)
parser.add_argument("--bucket_name", help="Name of the bucket", default=None)
parser.add_argument("--s3_endpoint_url", help="S3 endpoint URL", default=None)
parser.add_argument("--aws_access_key_id", help="AWS access key ID", default=None)
parser.add_argument("--aws_secret_access_key", help="AWS secret access key", default=None)
parser.add_argument("--object_size", help="Size of the objects in bytes", type=int, default=None)
parser.add_argument("--versions", help="Number of versions to be created", type=int, default=None)
parser.add_argument("--objects_count", help="Number of objects to be placed", type=int, default=None)
parser.add_argument("--object_prefix", help="Prefix for the objects", default=None)
parser.add_argument("--logging", help="Enable debug logging", action="store_true")
args = parser.parse_args()

# Rest of the script

if args.import_json:
    credentials = read_credentials_from_json(args.import_json)
    BUCKET_NAME = credentials["bucket_name"]
    S3_ENDPOINT_URL = credentials["s3_endpoint_url"]
    AWS_ACCESS_KEY_ID = credentials["aws_access_key_id"]
    AWS_SECRET_ACCESS_KEY = credentials["aws_secret_access_key"]
else:
    JSON_IMPORT = input("Do you want to import JSON file for configuration? (yes/no): ")
    if JSON_IMPORT.lower() == "yes":
        JSON_FILE_PATH = input("Enter the JSON file path: ")
        credentials = read_credentials_from_json(JSON_FILE_PATH)
        BUCKET_NAME = credentials["bucket_name"]
        S3_ENDPOINT_URL = credentials["s3_endpoint_url"]
        AWS_ACCESS_KEY_ID = credentials["aws_access_key_id"]
        AWS_SECRET_ACCESS_KEY = credentials["aws_secret_access_key"]
    else:
        if args.bucket_name:
            BUCKET_NAME = args.bucket_name
        else:
            BUCKET_NAME = input("Enter the bucket name: ")

        if args.s3_endpoint_url:
            S3_ENDPOINT_URL = args.s3_endpoint_url
        else:
            S3_ENDPOINT_URL = input("Enter the S3 endpoint URL, (EXAMPLE http://example.com:443): ")

        if args.aws_access_key_id:
            AWS_ACCESS_KEY_ID = args.aws_access_key_id
        else:
            AWS_ACCESS_KEY_ID = input("Enter the AWS access key ID: ")

        if args.aws_secret_access_key:
           AWS_SECRET_ACCESS_KEY = args.aws_secret_access_key
        else:
           AWS_SECRET_ACCESS_KEY = input("Enter the AWS secret access key: ")

if args.object_size:
    OBJECT_SIZE = args.object_size
else:
    OBJECT_SIZE = get_integer_input("Enter the size of the objects in bytes: ")

if args.versions is not None:
    VERSIONS = args.versions
else:
    VERSIONS = get_integer_input("Enter the number of versions to be created: ")

if args.objects_count:
    OBJECTS_COUNT = args.objects_count
else:
    OBJECTS_COUNT = get_integer_input("Enter the number of objects to be placed: ")

if args.object_prefix == 'None':
    OBJECT_PREFIX = None
else:
    OBJECT_PREFIX = args.object_prefix

# Set logging level
LOG_LEVEL = logging.DEBUG if args.logging else logging.INFO
file_logger.setLevel(LOG_LEVEL)

# Create an S3 client
s3 = boto3.client("s3",
                  verify=False,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  endpoint_url=S3_ENDPOINT_URL)

# Define a function that creates a single object in the bucket
def create_object(arg, q):
    try:
        # Generate a random object key with the prefix
        object_key = f"{OBJECT_PREFIX or ''}{str(uuid.uuid4())}"
        q.put(f"Generated object key: {object_key}")

        # Generate random content for the object
        object_content = os.urandom(OBJECT_SIZE)
        q.put(f"Generated object content of size: {len(object_content)}")

        # Put the object in the bucket
        response = s3.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=object_content)
        q.put(f"Put object {object_key} to the bucket with HTTP status: {response['ResponseMetadata']['HTTPStatusCode']}")

        # Create versions of the object
        for _ in range(VERSIONS):
            s3.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=object_content)
            q.put(f"Created version for object {object_key}")

        # Log the response
        q.put(f"Response: {response}")

        # Return the response
        return response

    except Exception as e:
        file_logger.error(f'Error creating object: {e}')
        return None

# Create a thread pool with 8 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    # Create a queue for the logging thread
    q = Queue()

    # Start the logging thread
    Thread(target=log_thread, args=(q,), daemon=True).start()

    # Use the thread pool to create objects in the bucket
    responses = [response for response in executor.map(create_object, range(OBJECTS_COUNT), [q]*OBJECTS_COUNT)]

    # Signal the logging thread to finish
    q.put(None)

    # Wait for all log messages to be processed
    q.join()
