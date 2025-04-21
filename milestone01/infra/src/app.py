import aws_cdk as cdk
from stacks.backend import BackendStack

app = cdk.App()

backendStack = BackendStack(app, "BackendStack")

app.synth()
