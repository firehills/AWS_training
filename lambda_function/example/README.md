* Lambda

Any language, only pay for compute time used

Conventaion to have lamda entry point with this signature

handler(event, context)

# create a new app - see https://docs.aws.amazon.com/cdk/v2/guide/cli.html
cdk init <TEMPLATE> --language <LANGUAGE>
eg
```shell
mkdir my-app; cd my-app
cdk init app --language python
```

my-app/app.py is entry, this list s the stacks

If you have issues deploying, in console delete the "Stack" under CloudFormation and the "Function" under "Lambda"

# to deploy ...
cdk deploy MyAppStack





