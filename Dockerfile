FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org  -r requirements.txt

ENTRYPOINT python3 -m flask run