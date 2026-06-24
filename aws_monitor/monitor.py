import json
import argparse
from services.ec2 import get_ec2_instances
from services.s3  import get_s3_buckets
from services.rds import get_rds_instances

def build_report(service):
    report = {}

    if service in ("all", "ec2"):
        report["ec2"] = get_ec2_instances()

    if service in ("all", "s3"):
        report["s3"] = get_s3_buckets()

    if service in ("all", "rds"):
        report["rds"] = get_rds_instances()

    return report

def print_report(report):
    print("\n=== AWS Infrastructure Monitor ===\n")

    if "ec2" in report:
        print("EC2 Instances:")
        if not report["ec2"]:
            print("  No instances found.")
        for i in report["ec2"]:
            print(f"  {i['id']} | {i['type']} | {i['state']} | {i['az']}")

    if "s3" in report:
        print("\nS3 Buckets:")
        if not report["s3"]:
            print("  No buckets found.")
        for b in report["s3"]:
            print(f"  {b['name']} | created: {b['created']} | objects: {b['objects']}")

    if "rds" in report:
        print("\nRDS Instances:")
        if not report["rds"]:
            print("  No RDS instances found.")
        for db in report["rds"]:
            print(f"  {db['id']} | {db['engine']} | {db['status']} | {db['class']}")

def save_report(report, filename="report.json"):
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved → {filename}")

def main():
    parser = argparse.ArgumentParser(description="AWS Infrastructure Monitor")
    parser.add_argument(
        "--service",
        choices=["all", "ec2", "s3", "rds"],
        default="all",
        help="Service to monitor"
    )
    parser.add_argument(
        "--output",
        default="report.json",
        help="Output filename for the report"
    )
    args = parser.parse_args()

    report = build_report(args.service)
    print_report(report)
    save_report(report, args.output)

if __name__ == '__main__':
    main()
