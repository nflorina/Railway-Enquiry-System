FROM python:3.6

WORKDIR /admin

COPY /admin/requirements.txt /admin
RUN pip install -r /admin/requirements.txt

COPY /admin/admin.py /admin
CMD python /admin/admin.py
