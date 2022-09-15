FROM eeacms/kgs:21.1.30
MAINTAINER "EEA: IDM2 B-Team"

ENV GRAYLOG_FACILITY=cca-plone

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
 && apt-get install build-essential bash-completion pkg-config software-properties-common \
 python-setuptools binutils libgdal-dev -y

RUN pip install numpy==1.16.4
RUN pip install pygdal==2.1.2.3 rsa==4.0 oauth2client
RUN pip install nltk==3.1

RUN python -m nltk.downloader -d /usr/local/share/nltk_data all

RUN buildout

COPY buildout.cfg /plone/instance/
RUN buildout -N
RUN chown -R plone /plone

RUN sed -i "s/debug-mode false/debug-mode true/" parts/zeo_client/etc/zope.conf
RUN sed -i "s/debug-mode false/debug-mode true/" /plone/instance/parts/zeo_client/etc/zope.conf
