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
