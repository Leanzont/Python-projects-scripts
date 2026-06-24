import boto3

def get_ec2_instances():
    ec2 = boto3.client('ec2', region_name='us-east-2')
    response = ec2.describe_instances()
    instances = []
    
    for reservation in response['Reservations']: #<---- 'Reservations' is the instances 
        for instance in reservation['Instances']:
            instances.append({
                "id":    instance['InstanceId'],
                "type":  instance['InstanceType'],
                "state": instance['State']['Name'],
                "az":    instance['Placement']['AvailabilityZone']
            })
    return instances 
