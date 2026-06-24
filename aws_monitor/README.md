# AWS Infrastructure Monitor

A command-line tool that queries live AWS infrastructure using Boto3 and generates a structured JSON report. Supports EC2, S3, and RDS — individually or all at once.

---

## How It Works

The monitor is built around three service modules that each query one AWS service and return a list of dictionaries. A central `monitor.py` entry point ties them together, prints the results to the terminal, and saves them to a JSON file.

```
python monitor.py --service all
python monitor.py --service ec2
python monitor.py --service s3
python monitor.py --service rds --output my_report.json
```

```
=== AWS Infrastructure Monitor ===

EC2 Instances:
  No instances found.

S3 Buckets:
  lean-23 | created: 2026-06-22 19:29:01+00:00 | objects: 0

RDS Instances:
  No RDS instances found.

Report saved → report.json
```

---

## Project Structure

```
aws_monitor/
├── monitor.py          # Entry point — argparse, orchestration, output
├── services/
│   ├── __init__.py     # Makes services/ a Python package
│   ├── ec2.py          # get_ec2_instances()
│   ├── s3.py           # get_s3_buckets()
│   └── rds.py          # get_rds_instances()
└── report.json         # Auto-generated after each run
```

---

## Tech Stack

- Python 3
- `boto3` — AWS SDK for Python
- `argparse` — CLI argument parsing
- `json` — structured report output

---

## Function Breakdown

### `services/ec2.py`— EC2 Instance Query

Calls `ec2.describe_instances()` and iterates through the response. AWS wraps instances inside `Reservations` — a legacy grouping that requires two nested loops: one for reservations, one for the instances inside each reservation.

```python
import boto3

def get_ec2_instances():
    ec2 = boto3.client('ec2', region_name='us-east-2')
    response = ec2.describe_instances()
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                "id":    instance['InstanceId'],
                "type":  instance['InstanceType'],
                "state": instance['State']['Name'],
                "az":    instance['Placement']['AvailabilityZone']
            })

    return instances
```

### `services/s3.py` — S3 Bucket Query

Calls `s3.list_buckets()` to get all buckets, then for each bucket calls `s3.list_objects_v2()` to count the objects inside. The `try/except` protects against buckets with restricted permissions — instead of crashing, it stores `"no access"` for that bucket.

```python
import boto3

def get_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = []

    for bucket in response["Buckets"]:
        name = bucket["Name"]
        try:
            obj_response = s3.list_objects_v2(Bucket=name)
            count = obj_response["KeyCount"]
        except Exception:
            count = "no access"

        buckets.append({
            "name":    name,
            "created": str(bucket["CreationDate"]),
            "objects": count
        })

    return buckets
```

### `services/rds.py` — RDS Instance Query

Calls `rds.describe_db_instances()` and extracts the instance list from the `DBInstances` key. Same pattern as EC2 and S3 — iterate the list and store each item as a dictionary.

```python
import boto3

def get_rds_instances(region="us-east-2"):
    rds = boto3.client('rds', region_name=region)
    response = rds.describe_db_instances()
    db_info = []

    for db in response['DBInstances']:
        db_info.append({
            "id":     db['DBInstanceIdentifier'],
            "engine": f"{db['Engine']} {db['EngineVersion']}",
            "status": db['DBInstanceStatus'],
            "class":  db['DBInstanceClass']
        })

    return db_info
```

### `build_report(service)` — Report Builder

Calls only the service functions that were requested. Returns a single dictionary with the results from each service as a key. This is the core of the script — everything flows through here.

```python
report = build_report("s3")
# output: {'s3': [{'name': 'lean-23', 'created': '...', 'objects': 0}]}

report = build_report("all")
# output: {'ec2': [], 's3': [...], 'rds': []}
```

### `print_report(report)` — Terminal Output

Takes the dictionary from `build_report()` and prints it in a readable format. For each service it checks whether the key exists in the report, then whether the list is empty, then iterates and prints each item.

```python
report = build_report("s3")
print_report(report)
```

```
=== AWS Infrastructure Monitor ===

S3 Buckets:
  lean-23 | created: 2026-06-22 19:29:01+00:00 | objects: 0
```

### `save_report(report, filename)` — JSON Export

Writes the full report dictionary to a JSON file using `json.dump()` with 2-space indentation.

### `main()` — Entry Point

Parses CLI arguments and calls the three functions in sequence: `build_report` → `print_report` → `save_report`. The `--service` argument uses `choices` to validate input automatically — argparse rejects any value outside `all`, `ec2`, `s3`, `rds` without extra validation code.

---

## Usage

```bash
# Monitor all services (default)
python monitor.py --service all

# Monitor a specific service
python monitor.py --service ec2
python monitor.py --service s3
python monitor.py --service rds

# Custom output filename
python monitor.py --service all --output infra_report.json
```

### CLI Arguments

|Argument|Required|Default|Description|
|---|---|---|---|
|`--service`|No|`all`|Service to query: `all`, `ec2`, `s3`, or `rds`|
|`--output`|No|`report.json`|Output filename for the JSON report|

---

## Example JSON Output

```json
{
  "ec2": [],
  "s3": [
    {
      "name": "lean-23",
      "created": "2026-06-22 19:29:01+00:00",
      "objects": 0
    }
  ],
  "rds": []
}
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

- AWS SDK usage with `boto3` across multiple services
- Modular project structure with a `services/` package
- Response parsing from nested AWS API dictionaries
- CLI argument parsing with `argparse` and `choices` validation
- Structured JSON report generation
- Error handling with `try/except` for restricted resources
