import boto3
from dotenv import load_dotenv


def get_boto_client(client_type: str):
    load_dotenv()
    # if aws configure is done, can grab client like this
    myclient = boto3.client(client_type)
    return myclient


# Parameters via AWS Systems Manager
client = get_boto_client('ssm')

response = client.get_parameters(
    Names=[
        'arn:aws:ssm:us-east-1:337018070967:parameter/ai-cop-backend-config'
    ],
)

print(response['Parameters'][0]['Name'] + " = " + response['Parameters'][0]['Value'])
