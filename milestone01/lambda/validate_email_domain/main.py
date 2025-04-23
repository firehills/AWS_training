# See also https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html


def lambda_handler(event, context):
    # It sets the user pool autoConfirmUser flag after validating the email domain
    event['response']['autoConfirmUser'] = False
  
    print(event)
    
    # Split the email address so we can compare domains
    address = event['request']['userAttributes']['email'].split('@')
    
    print("Got address " + address[1])

    if (address[1] == "gmail.com") or (address[1] == "hidglobal.com"):
        print("Domain Found")

        # skip verification for known domains
        event['response']['autoConfirmUser'] = True
        event['response']['autoVerifyEmail'] = True
        
    else:
        # unknow, invalid? dont allow them to register
        print("Domain NOT found - exception")
        raise Exception("AccessDenied: Email domain is not allowed")
    
    print(event)

    # Return to Amazon Cognito
    return event
    