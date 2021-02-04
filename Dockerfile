FROM python:3.8-alpine

# Install NinjaUri

ENV NINJAURI_HOME=/opt/NinjaUri

RUN adduser -Ds /bin/sh ninjauri \
    && mkdir -p ${NINJAURI_HOME}

COPY requirements.txt ${NINJAURI_HOME}
COPY ninjauri.py ${NINJAURI_HOME}
COPY ninjauri.sh ${NINJAURI_HOME}

RUN pip3 install -r ${NINJAURI_HOME}/requirements.txt \
    && chown -R ninjauri:ninjauri /usr/local/lib/python3.8/site-packages/tldextract \
    && ln -s ${NINJAURI_HOME}/ninjauri.py /usr/local/bin/ninjauri

USER ninjauri
WORKDIR /home/ninjauri

# Run NinjaUri

ENTRYPOINT ["/opt/NinjaUri/ninjauri.sh"]
CMD ["ninjauri", "-h"]
