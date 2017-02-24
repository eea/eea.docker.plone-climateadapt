FROM eeacms/kgs:9.1
MAINTAINER "EEA: IDM2 B-Team"

RUN apt-get update && apt-get install build-essential -y
COPY buildout.cfg /plone/instance/
RUN buildout
