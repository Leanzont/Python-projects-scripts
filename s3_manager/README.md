# Python S3 Manager

A command-line tool built with boto3 to interact with AWS S3 directly from the terminal.
Supports creating buckets, uploading files, and listing objects — with structured error handling for every operation.

---

## Features

- Create an S3 bucket in a specified region
- Upload a local file to a target bucket
- List all objects inside a bucket with metadata
- Pre-upload local file validation before making any AWS request
- Structured error handling using `ClientError` and `S3UploadFailedError`

---

## Tech Stack

- Python 3
- `boto3` — AWS SDK for Python
- `botocore` — low-level AWS exceptions (`ClientError`)
- `argparse` — CLI argument parsing
- `os` — local filesystem validation

---

## Project Structure

```
s3_manager/
├── s3_manager.py
└── README.md
```

---

## Function Breakdown

### `create_bucket(bucket_name, region)` — Bucket Creation
Initializes an S3 client scoped to the target region and creates the bucket using
`s3.create_bucket()`. Outside `us-east-1`, AWS requires the `LocationConstraint`
parameter inside `CreateBucketConfiguration` — without it the request fails.
Errors are caught via `ClientError` and the specific AWS message is extracted from
`e.response['Error']['Message']`.

### `list_objects(bucket_name)` — Object Listing
Calls `s3.list_objects_v2()` and extracts the object list using `.get("Contents", [])`.
When a bucket is empty, AWS omits the `Contents` key entirely from the response —
`.get()` falls back to an empty list `[]`, preventing a `KeyError`.
Each object is printed with its key, last modified timestamp, and size in bytes.
Errors are caught via `ClientError` using `e.response['Error']['Code']` to distinguish
between `NoSuchBucket` and `AccessDenied`.

### `upload_file(bucket_name, local_filepath, s3_object_name)` — File Upload
Validates the local file exists with `os.path.exists()` before making any AWS request.
Uses `s3.upload_file()` which manages the transfer using background threads —
this means failures raise `S3UploadFailedError` instead of `ClientError`.
The exception is converted to a string with `str(e)` and checked for
`'NoSuchBucket'` or `'AccessDenied'` substrings.

### `main()` — Entry Point
Parses three CLI arguments via `argparse`: `--action`, `--bucket`, and `--file`.
Routes to the correct function based on the action, validates required arguments
per operation, and prints a usage error if an unrecognized action is passed.
`RawDescriptionHelpFormatter` preserves the multi-line usage examples in the help text.

---

## Why Two Different Exception Types

`ClientError` (from `botocore`) handles most AWS API errors — bucket not found,
access denied, invalid parameters. However, `s3.upload_file()` runs transfers
on background threads, so AWS wraps any failure inside `S3UploadFailedError`
(from `boto3`). Both need to be imported and handled separately.

```python
from botocore.exceptions import ClientError       # API-level errors
from boto3.exceptions import S3UploadFailedError  # transfer-level errors
```

---

## Usage

```bash
# Create a bucket
python s3_manager.py --action create --bucket my-bucket-name

# Upload a file
python s3_manager.py --action upload --bucket my-bucket-name --file document.txt

# List objects in a bucket
python s3_manager.py --action list --bucket my-bucket-name
```

### CLI Arguments

| Argument   | Required | Description                                      |
|------------|----------|--------------------------------------------------|
| `--action` | ✅        | Operation to run: `create`, `upload`, or `list`  |
| `--bucket` | ✅        | Target S3 bucket name                            |
| `--file`   | ⚠️ upload | Local file path (required only for `upload`)     |

---

## Example Output

```
# Create
✅ Bucket 'my-bucket-name' created in us-east-2

# Upload
[+] 'document.txt' uploaded successfully.

# List
File Name: document.txt | Last Modified: 2026-06-09 21:34:02+00:00 | Size: 48
File Name: notes.txt    | Last Modified: 2026-06-09 21:43:54+00:00 | Size: 460
```

---

## Prerequisites

```bash
pip install boto3
```

AWS credentials must be configured locally:

```bash
aws configure
```

---

## Concepts Practiced

- AWS SDK usage with `boto3`
- S3 operations: bucket creation, file upload, object listing
- Structured error handling with `ClientError` and `S3UploadFailedError`
- Pre-flight local validation before making remote requests
- CLI argument parsing with `argparse`
- Response parsing from AWS API dictionaries
