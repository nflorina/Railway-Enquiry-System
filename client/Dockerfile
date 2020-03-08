FROM python:3.6

WORKDIR /client

COPY /client/requirements.txt /client
RUN pip install -r /client/requirements.txt

COPY /client/client.py /client
ENTRYPOINT ["python", "./client.py"]
