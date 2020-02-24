FROM python:3
MAINTAINER Isaac Sanchez <sanchezfs@sou.edu>

ENV INSTALL_PATH /gigavisor
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "gigavisor.app:create_app()"
