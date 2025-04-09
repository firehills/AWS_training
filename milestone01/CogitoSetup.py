import boto3
import os
from dotenv import load_dotenv

# open an authenticated client, looks for file .env in local dir that has the key flags set. 
def get_boto_client(client_type: str):
    load_dotenv()
    # if aws configure is done, can grab client like this
    myclient = boto3.client(client_type)
    return myclient


client = get_boto_client('cognito-idp')


def create_user_pool(client, u_p_name: str):
    response = client.create_user_pool(
        PoolName=u_p_name,
        Policies={           # Allow poor passwords - Good for testinf, BAD for real code
        'PasswordPolicy': {
            'MinimumLength': 6,
            'RequireUppercase': False,
            'RequireLowercase': False,
            'RequireNumbers': False,
            'RequireSymbols': False,
            'PasswordHistorySize': 0,
            'TemporaryPasswordValidityDays': 1
        },
        'SignInPolicy': {
            'AllowedFirstAuthFactors': [
                'PASSWORD'
            ]
        }
    }
    )
    return response




client = get_boto_client('cognito-idp')

# Create the user pool - You can have multiple pools with same name, but they get different autogen'd ID's 
#response = create_user_pool(client, "poolname_test01")
response = client.list_user_pools(
    NextToken="NextTokenOnlyReturnedIfAnotherPageOfResults",
    MaxResults=20
)

for pool in response["UserPools"]:
    print (pool)

