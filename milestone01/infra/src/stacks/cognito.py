import os
from pathlib import Path
from aws_cdk import aws_iam as iam
from aws_cdk import Stack, RemovalPolicy, CfnOutput
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as lambda_python

from constructs import Construct

# Setup  
#
class CognitoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get restrict domain function name from config
        validate_email_function_name = "lambda-restrict-domain"
        validate_email_function_path = Path(os.getcwd()).parent.joinpath("lambda/validate_email_domain")

        
        print("restrictlambda path at " + str(validate_email_function_name))
        domain_restrict_lambda = lambda_python.PythonFunction(
            self,
            validate_email_function_name,
            description="Function is to restrict external users to user pool; allow only hidglobal/assaabloy/gmail users.",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="lambda_handler",
            index="main.py",
            entry=str(validate_email_function_path),
        )

        # Grant Cognito permission to invoke the Lambda function
        domain_restrict_lambda.add_permission(
            "CognitoInvokeLambda",
            principal=iam.ServicePrincipal("cognito-idp.amazonaws.com"),
            action="lambda:InvokeFunction",
        )

        user_pool_name = "milestone1_userpool"

        user_pool = cognito.UserPool(
            self,
            user_pool_name,
            user_pool_name=user_pool_name,
            password_policy=cognito.PasswordPolicy(
                min_length=6,
                require_digits=False,
                require_lowercase=False,
                require_uppercase=False,
                require_symbols=False,
            ),
            mfa=cognito.Mfa.OFF,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True),
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            self_sign_up_enabled=True,
            removal_policy=RemovalPolicy.DESTROY,
            lambda_triggers=cognito.UserPoolTriggers(     # <- this to add a trigger
                pre_sign_up=domain_restrict_lambda,
            ),
        )

        # // or attach the Lambda as a trigger to the User Pool after creation
        # userPool.AddTrigger(UserPoolOperation.PRE_SIGN_UP, domain_restrict_lambda);


        user_pool_client = user_pool.add_client(
            "main-client",
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
        )

        # CfnOutput - CloudFormationOutput export objects for other stacks
        # Other stacks can import with Import with aws_cdk.Fn.importValue('<name>')) 
        _ = CfnOutput(
            self,
            "user_pool_id",
            value=user_pool.user_pool_id,
            description="The ID of the user pool",
        )

        _ = CfnOutput(
            self,
            "user_pool_client_id",
            value=user_pool_client.user_pool_client_id,
            description="The ID of the user pool client",
        )
