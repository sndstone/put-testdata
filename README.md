# put-test-data-into-S3-bucket

A Python 3 script that uploads randomized objects to an S3-compatible bucket using `boto3`. It can run fully interactive or accept command-line arguments (including a JSON config) to automate bulk test-data uploads with optional object versioning, checksums, and multithreading.

## Requirements

- Python 3
- `boto3`
- `prettytable` (imported; currently not used by the script)

## What the script does

- Reads S3 credentials and endpoint settings from either:
  - a JSON config file, or
  - command-line arguments, or
  - interactive prompts.
- Generates random object content of a fixed size (or reuses a single payload when `--simple_data` is set).
- Uploads a specified number of objects, optionally creating multiple versions for each object.
- Uses a pool of worker threads to upload concurrently.
- Calculates and sends a checksum per object if requested.
- Writes debug logs to `s3_upload.log` when `--debug` is enabled; prints summary/progress to stdout.

## Usage

### Interactive mode

Run without arguments to answer prompts:

```bash
python3 put-testdata.py
```

### Command-line mode

Provide settings as arguments:

```bash
python3 put-testdata.py \
  --bucket_name my-bucket \
  --s3_endpoint_url http://example.com:443 \
  --aws_access_key_id example-accesskey \
  --aws_secret_access_key example-secret \
  --object_size 1024 \
  --versions 4 \
  --objects_count 50 \
  --object_prefix testdata/ \
  --threads 16 \
  --checksum sha256
```

### JSON configuration

Provide a JSON file with connection details and override any values with command-line flags:

```json
{
  "bucket_name": "my-bucket",
  "s3_endpoint_url": "http://example.com:443",
  "aws_access_key_id": "example-accesskey",
  "aws_secret_access_key": "example-secret"
}
```

```bash
python3 put-testdata.py \
  --import_json credentials.json \
  --object_size 1024 \
  --versions 4 \
  --objects_count 50
```

## Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `--import_json` | string | none | Path to JSON file containing `bucket_name`, `s3_endpoint_url`, `aws_access_key_id`, `aws_secret_access_key`. |
| `--bucket_name` | string | interactive prompt | S3 bucket name to upload to. |
| `--s3_endpoint_url` | string | interactive prompt | S3 endpoint URL (e.g. `http://example.com:443`). |
| `--aws_access_key_id` | string | interactive prompt | AWS access key ID. |
| `--aws_secret_access_key` | string | interactive prompt | AWS secret access key. |
| `--object_size` | int | interactive prompt | Size of each object in bytes. |
| `--versions` | int | interactive prompt | Number of versions to create per object (0 disables versions). |
| `--objects_count` | int | interactive prompt | Number of objects to upload. |
| `--object_prefix` | string | empty | Prefix prepended to each generated object key. |
| `--threads` | int | `CPU count * 2` | Number of upload worker threads. |
| `--simple_data` | flag | false | Reuse a single generated payload for all uploads. |
| `--debug` | flag | false | Enable debug logging to `s3_upload.log`. |
| `--checksum` | string | `md5` | Checksum algorithm: `md5`, `crc32`, `crc32c`, `sha1`, `sha256`, or `none`. |

## Examples

### Upload 10 objects with no versioning

```bash
python3 put-testdata.py \
  --bucket_name my-bucket \
  --s3_endpoint_url http://example.com:443 \
  --aws_access_key_id example-accesskey \
  --aws_secret_access_key example-secret \
  --object_size 2048 \
  --versions 0 \
  --objects_count 10
```

### Reuse a single payload with CRC32C checksums

```bash
python3 put-testdata.py \
  --import_json credentials.json \
  --object_size 4096 \
  --versions 2 \
  --objects_count 100 \
  --simple_data \
  --checksum crc32c
```

### High-concurrency run with debug logging

```bash
python3 put-testdata.py \
  --import_json credentials.json \
  --object_size 1024 \
  --versions 1 \
  --objects_count 500 \
  --threads 32 \
  --debug
```

## Notes

- The script logs progress to stdout and writes detailed logs to `s3_upload.log` only when `--debug` is enabled.
- When `--simple_data` is enabled, a single random payload is generated once and reused for all uploads (including versions).
- The `--checksum none` option disables checksum calculation and request fields.
