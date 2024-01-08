import boto3
import concurrent.futures
import os
import uuid
from prettytable import PrettyTable
import json
import logging
from threading import Thread
from queue import Queue

# Setup logging
LOG_FILENAME = 's3_upload.log'
file_logger = logging.getLogger('file_logger')
file_logger.setLevel(logging.INFO)
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
    counter = 0
    while True:
        message = q.get()
        if message is None:
            break
        file_logger.info(message)
        if "Put object" in message:
            counter += 1
            print(f'\rUploaded {counter} objects', end='')
        q.task_done()

print(f"Logging to file {LOG_FILENAME} with level INFO")

# Asks inputs to run run the script
JSON_IMPORT = input("Do you want to import JSON file for configuration? (yes/no): ")

if JSON_IMPORT.lower() == "yes":
    JSON_FILE_PATH = input("Enter the JSON file path: ")
    credentials = read_credentials_from_json(JSON_FILE_PATH)
    BUCKET_NAME = credentials["bucket_name"]
    S3_ENDPOINT_URL = credentials["s3_endpoint_url"]
    AWS_ACCESS_KEY_ID = credentials["aws_access_key_id"]
    AWS_SECRET_ACCESS_KEY = credentials["aws_secret_access_key"]
else:
    BUCKET_NAME = input("Enter the bucket name: ")
    S3_ENDPOINT_URL = input("Enter the S3 endpoint URL, (EXAMPLE http://example.com:443): ")
    AWS_ACCESS_KEY_ID = input("Enter the AWS access key ID: ")
    AWS_SECRET_ACCESS_KEY = input("Enter the AWS secret access key: ")

def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

OBJECT_SIZE = get_integer_input("Enter the size of the objects in bytes: ")
VERSIONS = get_integer_input("Enter the number of versions to be created: ")
OBJECTS_COUNT = get_integer_input("Enter the number of objects to be placed: ")
OBJECT_PREFIX = input("Enter the prefix for the objects: ")

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
        object_key = f"{OBJECT_PREFIX}{str(uuid.uuid4())}"
        q.put(f"Generated object key: {object_key}")

        # Generate random content for the object
        object_content = os.urandom(OBJECT_SIZE)
        q.put(f"Generated object content of size: {len(object_content)}")

        # Put the object in the bucket
        response = s3.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=object_content)
        q.put(f"Put object {object_key} to the bucket")

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

# Create a table
table = PrettyTable()

# Add columns to the table
table.field_names = ["HTTP Status Code", "Request ID", "Host ID", "Version ID"]

# Iterate through the responses and add the information to the table
for response in responses:
    if response is not None:
        table.add_row([str(response['ResponseMetadata']['HTTPStatusCode']),
                       response['ResponseMetadata']['RequestId'],
                       response['ResponseMetadata']['HostId'],
                       response.get("VersionId", "Not provided")])

# Print the table
print(table)
