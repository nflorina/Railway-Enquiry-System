FROM python:3.6

WORKDIR /client

COPY requirements.txt /client
RUN pip install -r requirements.txt

COPY client.py /client
ENTRYPOINT ["python", "./client.py"]
