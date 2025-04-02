# AWS_training
Learnings from AWS / Cloud interaction training


```shell
pip install --upgrade pip
python3 -m venv .venv 
source .venv/bin/activate
pip install --upgrade pip

python3 -m pip install -r requirements.txt
```

# Handy - show installed dependencies
python3 -m pip freeze


# setup/authrize local user for this app
aws configure 
ID eg AKIAUxxxxxxxxxxxxVW3
Key eg 78xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxf
region eg us-east-1
format (none)

aws sts get-caller-identity -> should give you a known user as per above 




# Lambda 

Any language, only pay for compute time used

Conventaion to have lamda entry point with this signature

handler(event, context)

## Lambda - Create New App

see https://docs.aws.amazon.com/cdk/v2/guide/cli.html

cdk init \<TEMPLATE\> --language \<LANGUAGE\>
eg
```shell
mkdir lambda_example; cd lambda_example
cdk init --list  # shows availible options/languages
cdk init app --language python
```

See lambda_example/lambda_example/lambda_example_stack.py - where we call Function() you create the lambda itself. Note that the "handler" and "code" must point to your function. in this example the business code is outside of the stack creation, lambda_function/example/main.py


lambda_example/app.py is entry, this lists the stacks, you can have more than 1 stack deployed here. 

If you have issues deploying, in console delete the "Stack" under CloudFormation and the "Function" under "Lambda"
```sh
## Deploy App
cd lambda_example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk list  # the stacks you can CAN deploy
cdk deploy LambdaExampleStack # and deploy 
```

## Lambda - Delete/Destory

From the AWS GUI
The stack is under  CloudFormation->Stacks - use Actions to delete.

the lambda functions themselves uder Lambda->Functions - use Actions to delete.

