FROM ubuntu:xenial

RUN apt-get -y -qq update
RUN apt-get -y -qq install python3 python3-pip nginx
RUN mkdir -p /var/www/adminstatic/ /var/www/userstatic/ /var/www/static/user/ /var/www/static/admin/ /opt/app/templates/ /var/www/static/global/

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

ADD app.py /opt/app/app.py
ADD templates/* /opt/app/templates/
ADD nginx.conf /etc/nginx/nginx.conf
ADD run.sh /opt/app/run.sh
ADD static/global/* /var/www/static/global/
ADD static/user/* /var/www/static/user/
ADD static/admin/* /var/www/static/admin/

RUN chmod -R 755 /var/www/static/*

CMD ["bash", "/opt/app/run.sh"]
