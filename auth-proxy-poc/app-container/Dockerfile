FROM python:3-alpine
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
run mkdir -p /opt/static-proxy/templates
ADD ./app.py /opt/static-proxy
ADD ./templates/* /opt/static-proxy/templates/
WORKDIR /opt/static-proxy
CMD ["python3", "app.py"]
