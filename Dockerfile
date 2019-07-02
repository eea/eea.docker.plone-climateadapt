FROM eeacms/kgs:19.4.10
MAINTAINER "EEA: IDM2 B-Team"

ENV GRAYLOG_FACILITY=cca-plone

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
 && apt-get install build-essential bash-completion pkg-config software-properties-common \
 python-setuptools binutils libgdal-dev -y

RUN pip install pygdal==2.1.2.3 oauth2client numpy==1.16.4

RUN buildout

COPY buildout.cfg /plone/instance/
RUN buildout -N
