FROM ubuntu:18.04
LABEL maintainer="philip@grassbag.net"
RUN apt-get update && \
    apt install -y python python-pip vim && \
    pip install --upgrade pip==9.0.3 && \
    pip install requests falcon gunicorn
COPY app /app
CMD ls / ; cd /app; gunicorn -b 0.0.0.0:38000 app:api --reload
EXPOSE 38000
