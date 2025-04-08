import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_validate_signup_email_domain.lambda_validate_signup_email_domain_stack import LambdaValidateSignupEmailDomainStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_validate_signup_email_domain/lambda_validate_signup_email_domain_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaValidateSignupEmailDomainStack(app, "lambda-validate-signup-email-domain")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
