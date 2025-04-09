import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# EG created console in AWS Secrets Manager -> Secrets
secret_name = "/ai-cop/the-secret"


def get_boto_client(client_type: str):
    load_dotenv()
    # if aws configure is done, can grab client like this
    myclient = boto3.client(service_name=client_type)
    return myclient


# Parameters via AWS Systems Manager
client = get_boto_client('secretsmanager')

try:
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
   
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print("The requested secret " + secret_name + " was not found")
    elif e.response['Error']['Code'] == 'InvalidRequestException':
        print("The request was invalid due to:", e)
    elif e.response['Error']['Code'] == 'InvalidParameterException':
        print("The request had invalid params:", e)
    elif e.response['Error']['Code'] == 'DecryptionFailure':
        print("The requested secret can't be decrypted using the provided KMS key:", e)
    elif e.response['Error']['Code'] == 'InternalServiceError':
        print("An error occurred on service side:", e)
else:
   
    # Secrets Manager decrypts the secret value using the associated KMS CMK
    # Depending on whether the secret was a string or binary, only one of these fields will be populated
    if 'SecretString' in get_secret_value_response:
        text_secret_data = get_secret_value_response['SecretString']
        binary_secret_data = None
    else:
        binary_secret_data = get_secret_value_response['SecretBinary']
        text_secret_data = None

    if text_secret_data:
        print(text_secret_data)
    if binary_secret_data: 
        print(binary_secret_data)



