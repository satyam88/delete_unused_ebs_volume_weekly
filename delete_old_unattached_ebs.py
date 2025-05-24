import boto3
from datetime import datetime, timezone, timedelta

def get_all_regions():
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions(AllRegions=False)
    return [region['RegionName'] for region in regions['Regions']]

def delete_old_unattached_volumes(region, days_old=30):
    ec2 = boto3.client('ec2', region_name=region)
    paginator = ec2.get_paginator('describe_volumes')

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days_old)

    for page in paginator.paginate(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    ):
        for volume in page['Volumes']:
            create_time = volume['CreateTime']
            volume_id = volume['VolumeId']

            if create_time < cutoff:
                print(f"🗑️ Deleting Volume: {volume_id} (Region: {region}, Created: {create_time})")
                try:
                    ec2.delete_volume(VolumeId=volume_id)
                    print(f"✅ Deleted volume {volume_id}")
                except Exception as e:
                    print(f"❌ Failed to delete {volume_id}: {str(e)}")

def main():
    regions = get_all_regions()
    print(f"🌍 Enabled AWS Regions: {regions}")

    for region in regions:
        print(f"\n🔍 Scanning region: {region}")
        delete_old_unattached_volumes(region)

if __name__ == "__main__":
    main()
