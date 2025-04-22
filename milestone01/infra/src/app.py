import aws_cdk as cdk
from stacks.backend import BackendStack
from stacks.cognito import CognitoStack


app = cdk.App()

cognitoStack = CognitoStack(app, "CognitoStack")
backendStack = BackendStack(app, "BackendStack")

app.synth()
