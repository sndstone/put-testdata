import boto3
import concurrent.futures
import os
import uuid
from prettytable import PrettyTable
import json

# Function to read credentials from JSON file
def read_credentials_from_json(file_path):
    with open(file_path, "r") as json_file:
        credentials = json.load(json_file)
        return credentials

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

OBJECT_SIZE = int(input("Enter the size of the objects in bytes: "))
VERSIONS = int(input("Enter the number of versions to be created: "))
OBJECTS_COUNT = int(input("Enter the number of objects to be placed: "))
OBJECT_PREFIX = input("Enter the prefix for the objects: ")

# Create an S3 client
s3 = boto3.client("s3",
                  verify=False,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  endpoint_url=S3_ENDPOINT_URL)

# Define a function that creates a single object in the bucket
def create_object(arg):
    # Generate a random object key with the prefix
    object_key = f"{OBJECT_PREFIX}{str(uuid.uuid4())}"

    # Generate random content for the object
    object_content = os.urandom(OBJECT_SIZE)

    # Put the object in the bucket
    response = s3.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=object_content)

    # Create versions of the object
    for j in range(VERSIONS):
        s3.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=object_content)

    # Return the response
    return response

# Create a thread pool with 4 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # Use the thread pool to create objects in the bucket
    responses = [response for response in executor.map(create_object, range(OBJECTS_COUNT))]

# Create a table
table = PrettyTable()

# Add columns to the table
table.field_names = ["HTTP Status Code", "Request ID", "Host ID", "Version ID"]

# Iterate through the responses and add the information to the table
for response in responses:
    table.add_row([str(response['ResponseMetadata']['HTTPStatusCode']),
                   response['ResponseMetadata']['RequestId'],
                   response['ResponseMetadata']['HostId'],
                   response.get("VersionId", "Not provided")])

# Print the table
print(table)
