import os
import argparse
import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError

def create_bucket(bucket_name, region="us-east-2"):
    s3 = boto3.client('s3', region_name=region)
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
        print(f"¡Success! Bucket '{bucket_name}' created in {region}")
    except ClientError as e: 
        print(f"Error: {e.response['Error']['Message']}")
    
def upload_file(bucket_name, local_filepath, s3_object_name):
    if not os.path.exists(local_filepath):
        print(f"❌ Local Error: The file '{local_filepath}' does not exist on your computer.")
        return False

    try:
        s3 = boto3.client('s3', region_name='us-east-2')
        s3.upload_file(local_filepath, bucket_name, s3_object_name)
        print(f"[+] '{s3_object_name}' uploaded successfully.")
        return True
    except S3UploadFailedError as e:
        error_msg = str(e)
        if 'NoSuchBucket' in error_msg:
            print("❌ The bucket does not exist.")
        elif 'AccessDenied' in error_msg:
            print("❌ No write permissions on the bucket.")
        else:
            print(f"⚠️ Upload failed: {error_msg}")
        return False

def list_objects(bucket_name):
    try: 
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket_name)

        list_ob = response.get("Contents", [])
        if not list_ob:
            print("ℹ️  the bucket is empty.")
            return
            
        for li in list_ob:
            print(f"File Name: {li['Key']} | Last Modified: {li['LastModified']} | Size: {li['Size']}")
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            print("❌ The specified bucket does not exist.")
        elif error_code == 'AccessDenied':
            print("❌ You do not have permission to list this bucket.")
        else:
            print(f"⚠️ Error de AWS: {error_code}")

def main():
    parse = argparse.ArgumentParser(
        description=""" boto3 tool to create, upload, and list S3 buckets.
                        Usage examples:
                        List items:   python script.py --action list --bucket my-bucket-name
                        Upload file:  python script.py --action upload --bucket my-bucket-name --file document.txt
                        Create bucket: python script.py --action create --bucket my-bucket-name""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parse.add_argument("--action", type=str, help="Action options: 'create', 'list' or 'upload'")
    parse.add_argument("--bucket", type=str, help="Target S3 bucket name")
    parse.add_argument("--file", type=str, help="Local file path to upload (required for 'upload')")
    args = parse.parse_args()
    
    if args.action == 'create':
        if not args.bucket:
            print("❌ Error: --bucket is required for create")
            return
        create_bucket(args.bucket)
        
    elif args.action == 'upload':
        if not args.bucket or not args.file:
            print("❌ Error: Both --bucket and --file are required for upload")
            return
        upload_file(args.bucket, args.file, os.path.basename(args.file))
        
    elif args.action == 'list':
        if not args.bucket:
            print("❌ Error: --bucket is required to list objects")
            return
        list_objects(args.bucket)

    else:
        print("❌ Error: Please specify a valid --action ('create', 'upload', or 'list')")

if __name__ == '__main__':
    main()
