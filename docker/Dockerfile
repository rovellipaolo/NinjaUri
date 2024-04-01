FROM python:3.12-alpine

ENV NINJAURI_HOME=/opt/NinjaUri
ENV NINJAURI_USER=ninjauri

# Install NinjaUri

RUN adduser -Ds /bin/sh ${NINJAURI_USER} \
    && mkdir -p ${NINJAURI_HOME}

COPY requirements/ ${NINJAURI_HOME}/requirements/
COPY requirements.txt ${NINJAURI_HOME}
COPY ninjauri.py ${NINJAURI_HOME}

#RUN pip3 install -r ${NINJAURI_HOME}/requirements/prod.txt \
RUN pip3 install -r ${NINJAURI_HOME}/requirements.txt \
    && chown -R ninjauri:ninjauri /usr/local/lib/python3.12/site-packages/tldextract \
    && ln -s ${NINJAURI_HOME}/ninjauri.py /usr/local/bin/ninjauri

USER ninjauri
WORKDIR /home/ninjauri

# Run NinjaUri

CMD ["ninjauri", "-h"]
