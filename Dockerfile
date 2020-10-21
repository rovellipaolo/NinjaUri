FROM python:3.6-slim-stretch

# Install dependencies
RUN apt update && \
    apt install -qy python3 python3-pip

# Install NinjaUri
ENV NINJAURI_HOME=/opt/NinjaUri

RUN useradd -ms /bin/bash ninjauri && \
    mkdir -p ${NINJAURI_HOME}

COPY requirements.txt ${NINJAURI_HOME}
COPY ninjauri.py ${NINJAURI_HOME}
COPY ninjauri.sh ${NINJAURI_HOME}
COPY tests/ ${NINJAURI_HOME}/tests/

RUN pip3 install -r ${NINJAURI_HOME}/requirements.txt && \
    chown -R ninjauri:ninjauri /usr/local/lib/python3.6/site-packages/tldextract && \
    ln -s ${NINJAURI_HOME}/ninjauri.py /usr/local/bin/ninjauri

USER ninjauri
WORKDIR /home/ninjauri

# Run NinjaUri
ENTRYPOINT ["/opt/NinjaUri/ninjauri.sh"]
CMD ["ninjauri", "-h"]
