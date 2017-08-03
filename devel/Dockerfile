FROM eeacms/kgs:devel
MAINTAINER "EEA: IDM2 B-Team"

RUN curl -o /plone/instance/buildout.cfg -SL https://raw.githubusercontent.com/Petchesi-Iulian/eea.docker.plone-climateadapt/master/buildout.cfg
RUN buildout
