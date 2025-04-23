# infra
use CDK to deploy a backend application 


cd AWS_training/milestone01/infra


# check identify setup, use "aws configure" if not
aws sts get-caller-identity

# Local env
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
# Deploy operations

```sh
# Show deployable stacks - handy to make sure no coding errors
cdk list 
```

And to deploy ...

```sh
cdk deploy --all
cdk deploy <StackName>
cdk ls            # list all stacks in the app
cdk synth <name>  # emits the synthesized CloudFormation template
cdk deploy        # deploy this stack to your default AWS account/region
cdk diff          # compare deployed stack with current state
cdk docs          # open CDK documentation
```

