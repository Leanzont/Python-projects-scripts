import boto3

def get_rds_instances(region="us-east-2"):
    rds = boto3.client('rds', region_name=region)
    response = rds.describe_db_instances()
    db_info= []
    list_db = response['DBInstances'] # <---- this is key: DBInstances for access to value
    for db in list_db:
        db_info.append[{
            "id":        db['DBInstanceIdentifier'],
            "engine": f"{db['Engine']} {db['EngineVersion']}",
            "status":    db['DBInstanceStatus'],
            "class":     db['DBInstanceClass']
        }]
    return db_info
