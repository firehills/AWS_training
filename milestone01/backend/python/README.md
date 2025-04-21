# Basic Example - Simple Webserver App

## Run/test locally
```sh
python3 -m venv .venv 
source .venv/bin/activate
python3 -m pip install -r requirements.txt

fastapi dev main.py # = dev mode, use `fastapi run <name>` for production
```


## Run in Docker
```sh
# Build and rename to backend01
docker build -t backend01 .     

# run and remove on exit 
docker run --rm -p 127.0.0.1:8000:8000 backend01
```