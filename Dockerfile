FROM eeacms/kgs:18.7.29
MAINTAINER "EEA: IDM2 B-Team"

ENV GRAYLOG_FACILITY=cca-plone

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
 && apt-get install build-essential bash-completion pkg-config software-properties-common \
 python-software-properties python-setuptools binutils libgdal-dev libgdal1-dev -y

RUN pip install pygdal==1.10.1 oauth2client

RUN buildout

COPY buildout.cfg /plone/instance/
RUN buildout -N
