FROM python:3.8

MAINTAINER NullYing "ourweijiang@gmail.com"

RUN mkdir -p /var/www/gdst_news
WORKDIR /var/www/gdst_news

#设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone
ADD requirements.txt .

RUN echo '[global]\ntrusted-host=mirrors.aliyun.com\nindex-url=https://mirrors.aliyun.com/pypi/simple' > /etc/pip.conf && \
    pip install -U pip && pip install -r requirements.txt

ADD . /var/www/gdst_news
