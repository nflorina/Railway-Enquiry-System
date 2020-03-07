FROM python:3.6

WORKDIR /admin

COPY requirements.txt /admin
RUN pip install -r requirements.txt

COPY admin.py /admin
CMD python admin.py
