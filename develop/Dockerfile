FROM laszlocseh/eea.docker.plone-climateadapt:plone6

RUN runDeps="vim tmux mc" \
 && apt-get update \
 && apt-get install -y --no-install-recommends $runDeps \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY sources.ini /app/

RUN bin/pip install "mxdev>=3.0.0" \
 && bin/mxdev -c sources.ini \
 && bin/pip install -r requirements-mxdev.txt \
 && find /app -not -user plone -exec chown plone:plone {} \+