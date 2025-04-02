from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput
    # aws_sqs as sqs,
)

from constructs import Construct
from aws_cdk import aws_lambda as _lambda
from pathlib import Path

class LambdaExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

       
        # derive relative path to our actual lambda function
        path_to_functions_dir = (
            Path(__file__).parent.parent.parent / "lambda_function" / "example" 
        )

        print(path_to_functions_dir)

        # see https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.Function.html
        ex1_lambda = _lambda.Function(
            self,
            "lambda-ex1-id",                                                    # id string 
            description="This is the most basic hello world lambda function",   # A description of the function.
            runtime=_lambda.Runtime.PYTHON_3_13,                                # The runtime environment for the Lambda function that you are uploading.
            handler="main.handler",                                             # The name of the method within your code that Lambda calls to execute your function.
            code=_lambda.Code.from_asset(str(path_to_functions_dir)),           # The source code of your Lambda function.
        )

        fn_url = ex1_lambda.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)
        CfnOutput(self, "lambda-ex1-url", value=fn_url.url)

