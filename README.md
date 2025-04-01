# AWS_training
Learnings from AWS / Cloud interaction training


```shell
pip install --upgrade pip
python -m venv .venv 
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





