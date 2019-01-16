FROM python:3.6.5

MAINTAINER NullYing "ourweijiang@gmail.com"

RUN mkdir -p /var/www/gdst_news
WORKDIR /var/www/gdst_news

#设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone
ADD requirements.txt .
# RUN pip install -U pip && pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip install -U pip && pip install -r requirements.txt

ADD . /var/www/gdst_news
