import boto3
import os
from dotenv import load_dotenv


CLIENT_POOL_NAME: str  = "milestone01"
USER_EMAIL: str = "hill.philip@gmail.com"


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

response = client.list_user_pools(
    NextToken="NextTokenOnlyReturnedIfAnotherPageOfResults",
    MaxResults=20
)

#print(response)

# Did we get ALL entries, or need to deal with pages???
more_pages = 'NextToken' in response;
if more_pages:
    print('Found more pages - NextToken = ' + response['NextToken'])
    # TODO need to iterate round the pages, for the moment assume its all in 1 page......

# Does our pool exist? - if not create it
pool_id = ""
for pool in response["UserPools"]:
    print ('Name ' + pool['Name'] + ', ID = ' + pool['Id'])
    if pool['Name'] == CLIENT_POOL_NAME:
        pool_id = pool['Id']

# empty ID?
if not pool_id:
    # Create the user pool - You can have multiple pools with same name, but they get different autogen'd ID's 
    print("Create Pool " + CLIENT_POOL_NAME)
    response_create = create_user_pool(client, CLIENT_POOL_NAME)
else:
    print("Pool " + CLIENT_POOL_NAME + " Already Exists")




print("Using PoolID " + pool_id)

# does user exist? search for a specific email...
user_response = client.list_users(
    UserPoolId=pool_id,
    Filter="email = \"" + USER_EMAIL + "\"",
)

#print(user_response)
#print("")
#print(user_response['Users'])


# Email should be unique within a user pool, so dhould get back just 1 user
if len(user_response['Users']) == 1:
    print("Found User - UserName=" + user_response['Users'][0]['Username'])

    # (Attributes is a list of dictionary items, use Name to find the named attribute you want)
    for attribute in user_response['Users'][0]['Attributes']:
        if attribute['Name'] == 'email':
            print('Email=' + attribute['Value'])
else:
    # so create the user...?
    print("Did not find user ")