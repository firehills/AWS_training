FROM python:3.13.3-bookworm

# root at which local cmds will run from 
WORKDIR /project

ADD . /project/backend

RUN pip install -r /project/backend/requirements.txt

CMD ["fastapi", "dev","--host", "0.0.0.0", "/project/backend/main.py"]

EXPOSE 8000