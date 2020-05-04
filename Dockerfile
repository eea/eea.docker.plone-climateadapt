FROM eeacms/kgs:20.4.28
MAINTAINER "EEA: IDM2 B-Team"

ENV GRAYLOG_FACILITY=cca-plone

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
 && apt-get install build-essential bash-completion pkg-config software-properties-common \
 python-setuptools binutils libgdal-dev -y

RUN pip install numpy==1.16.4
RUN pip install pygdal==2.1.2.3 oauth2client

RUN buildout

COPY buildout.cfg /plone/instance/
RUN buildout -N
RUN chown -R plone /plone
