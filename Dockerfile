FROM eeacms/kgs:9.1
MAINTAINER "EEA: IDM2 B-Team"

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && apt-get install build-essential -y && apt-get install pkg-config && apt-get install bash-completion
RUN apt-get install software-properties-common python-software-properties -y
RUN apt-get install -y python-setuptools && apt-get install binutils -y
RUN wget -O- https://bootstrap.pypa.io/get-pip.py | python 
RUN pip install --upgrade setuptools && pip install --upgrade virtualenv

RUN apt-get install libgdal-dev -y && pip install pygdal==1.10.1

COPY buildout.cfg /plone/instance/
RUN buildout
