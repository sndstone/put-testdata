# put-test-data-into-S3-bucket
A Python3 script that Puts random objects into a bucket using boto3.

To run the script install boto3 and prettytable (used to table the output).

Select the size, amount of versions, how many objects and wait for the bucket to fill up with randomized test data:
* Enter the bucket name: my-bucket2000
* Enter the S3 endpoint URL including http// - https://: http://example.com:10444
* Enter the AWS access key ID: example-accesskey
* Enter the AWS secret access key: example-sxecretkey
* Enter the size of the objects in bytes: 1024
* Enter the number of versions to be created: 4
* Enter the number of objects to be placed: 50

The output will be a table containing all placed object within the bucket.
This project is still a work in progress so if you have any ideas or improvements please let me know or add them to the project.
