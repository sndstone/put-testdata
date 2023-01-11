# put-test-data-into-S3-bucket
Put test data into a bucket using boto3.
Select the size, amount of versions, how many objects and wait for the bucket to fill up with randomized test data:
-Enter the bucket name: my-bucket2000
-Enter the S3 endpoint URL including http// - https://: http://example.com:10444
-Enter the AWS access key ID: example-accesskey
-Enter the AWS secret access key: example-sxecretkey
-Enter the size of the objects in bytes: 1024
-Enter the number of versions to be created: 4
-Enter the number of objects to be placed: 50


The output will be a table containing all placed object within the bucket, example:
+------------------+------------------+----------+--------------------------------------------------+
| HTTP Status Code |    Request ID    | Host ID  |                    Version ID                    |
+------------------+------------------+----------+--------------------------------------------------+
|       200        | 1673435929306007 | 12393772 | NjgzQTkyNUEtOTFDNy0xMUVELThFNUUtNUM0QTAwQkQxRDJD |
|       200        | 1673435943778903 | 12868968 | NjgzQUE5MEMtOTFDNy0xMUVELTgwNzgtRUJFMDAwQzQ1RDY4 |
|       200        | 1673435902252816 | 12153580 | NjgzQjA1ODItOTFDNy0xMUVELTgzOEItMUZCNTAwQjk3MkVD |
|       200        | 1673435902302812 | 12136612 | NjgzQ0I4REMtOTFDNy0xMUVELTk2NjgtNzg3NDAwQjkzMEE0 |
|       200        | 1673435943778903 | 12868968 | Njg3MTZERjItOTFDNy0xMUVELTg2RkMtMjg2QzAwQzQ1RDY4 |
|       200        | 1673435902302812 | 12136612 | Njg3MjU5MzgtOTFDNy0xMUVELTgzNTItMkZFMzAwQjkzMEE0 |
|       200        | 1673435902698354 | 12136612 | Njg3NDM0QzQtOTFDNy0xMUVELTkxREUtN0Q5QjAwQjkzMEE0 |
|       200        | 1673435929278464 | 12153580 | Njg3NTg1RjQtOTFDNy0xMUVELThBMjYtOTZGMjAwQjk3MkVD |
|       200        | 1673438632361718 | 12393772 | Njg3QUQxRDAtOTFDNy0xMUVELTkwRTUtNzIwNDAwQkQxRDJD |
|       200        | 1673435943778903 | 12868968 | Njg3QUZFMzAtOTFDNy0xMUVELTlDRjQtQUVGMzAwQzQ1RDY4 |
|       200        | 1673435902189660 | 12868968 | Njg3RDc0OUUtOTFDNy0xMUVELTlDNkMtM0VEQzAwQzQ1RDY4 |
|       200        | 1673435929251308 | 12136612 | Njg3RUUxM0EtOTFDNy0xMUVELTk4NDMtODZGMDAwQjkzMEE0 |
|       200        | 1673435943636461 | 12153580 | Njg4NEY5NTgtOTFDNy0xMUVELTgzRTktMzBDQTAwQjk3MkVD |
|       200        | 1673435902302812 | 12136612 | Njg4NTVERUUtOTFDNy0xMUVELTg2NzUtQjg2QTAwQjkzMEE0 |
|       200        | 1673438631509163 | 12393772 | Njg4N0FBNDAtOTFDNy0xMUVELTk1RjctQzA4NTAwQkQxRDJD |
|       200        | 1673435929306007 | 12393772 | Njg4OEY5NUUtOTFDNy0xMUVELThGQzMtRDFFNDAwQkQxRDJD |
|       200        | 1673435943656160 | 12393772 | Njg4RjNFRUEtOTFDNy0xMUVELTk1NjAtOEY3NTAwQkQxRDJD |
|       200        | 1673435902302812 | 12136612 | Njg4RjE0NDItOTFDNy0xMUVELTgxREMtNzMxQzAwQjkzMEE0 |
|       200        | 1673435902189660 | 12868968 | Njg5MTI0M0EtOTFDNy0xMUVELTgzMjUtNDE1NDAwQzQ1RDY4 |
|       200        | 1673435929251308 | 12136612 | Njg5MzJDNkMtOTFDNy0xMUVELTg5MjQtRTA5RjAwQjkzMEE0 |
|       200        | 1673435902302812 | 12136612 | Njg5OEUzNzgtOTFDNy0xMUVELTk2RUUtQTUyNjAwQjkzMEE0 |
|       200        | 1673435943636461 | 12153580 | Njg5OTFDNkMtOTFDNy0xMUVELThDMkEtQjM5QTAwQjk3MkVD |
+------------------+------------------+----------+--------------------------------------------------+

Current project is a work in progress so if you have any ideas to improve please let them know and add them to the project.
