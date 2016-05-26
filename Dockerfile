FROM eeacms/kgs:6.7
MAINTAINER "EEA: IDM2 B-Team"

COPY buildout.cfg /plone/instance/
RUN buildout
