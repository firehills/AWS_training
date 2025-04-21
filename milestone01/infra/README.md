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
cdk deploy
cdk deploy <StackName>
```

