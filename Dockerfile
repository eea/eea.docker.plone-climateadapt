FROM eeacms/kgs:21.1.30
MAINTAINER "EEA: IDM2 B-Team"

ENV GRAYLOG_FACILITY=cca-plone

#Update stretch repositories
RUN sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list
RUN sed -i 's|security.debian.org|archive.debian.org/|g' /etc/apt/sources.list
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
 && apt-get install build-essential bash-completion pkg-config software-properties-common \
 python-setuptools binutils libgdal-dev -y

RUN pip install numpy==1.16.4
RUN pip install pygdal==2.1.2.3 rsa==4.0 oauth2client

RUN buildout

COPY buildout.cfg /plone/instance/
RUN buildout
# -N
#RUN chown -R plone /plone/
