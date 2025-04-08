
import boto3
import os
from dotenv import load_dotenv

# open an authenticated client, looks for file .env in local dir that has the key flags set. 
def get_boto_client():
    load_dotenv()
    
    
    # aws configure?, if not you need to specify ID's here
    #myclient = boto3.client('s3',
    #                  aws_access_key_id = os.environ.get("AWS_SERVER_PUBLIC_KEY"), 
    #                  aws_secret_access_key = os.environ.get("AWS_SERVER_SECRET_KEY"), 
    #                  region_name = os.environ.get("REGION_NAME"))
    

    # if aws configure is done, can grab client like this
    myclient = boto3.client('s3')


    return myclient


def s3_list_buckets():
    # Create an S3 client
    s3 = get_boto_client()

    # Call S3 to list current buckets
    response = s3.list_buckets()

    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    # Print out the bucket list
    print("Bucket List: %s" % buckets)
    return
    
def s3_create_bucket(bucket_name: str):
    # Create an S3 client
    s3 = get_boto_client()
    response = s3.create_bucket(Bucket=bucket_name)
    return

def s3_delete_bucket(bucket_name: str):
    # Create an S3 client
    s3 = get_boto_client()
    response = s3.delete_bucket(Bucket=bucket_name)
    return




    