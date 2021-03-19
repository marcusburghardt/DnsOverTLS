FROM centos:latest
MAINTAINER Marcus Burghardt "marcus.apb@gmail.com"

RUN yum update -y && \
    yum install -y python3
COPY ./dnsOverTLSProxy.py /app.py

WORKDIR /
EXPOSE 53/tcp
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]