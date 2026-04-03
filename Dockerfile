FROM eeacms/plone-backend:6.1.3-13

RUN runDeps="vim tmux mc" \
  && apt-get update \
  && apt-get install -y --no-install-recommends $runDeps \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt constraints.txt sources.ini /app/
COPY ./etc/zodbpack.conf /app/etc/zodbpack.conf

RUN ./bin/pip install -r requirements.txt -c constraints.txt ${PIP_PARAMS} \
 && find /app -not -user plone -exec chown plone:plone {} \+
