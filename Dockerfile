FROM python:3.5-slim-stretch

ENV NINJAURI_DIR=/opt/NinjaUri

RUN useradd -ms /bin/bash ninjauri

# Install dependencies
RUN apt update && \
    apt install -qy python3 python3-pip

# Install NinjaUri
RUN mkdir -p ${NINJAURI_DIR}
COPY requirements.txt ${NINJAURI_DIR}
COPY ninjauri.py ${NINJAURI_DIR}
COPY tests/ ${NINJAURI_DIR}/tests/

RUN pip3 install -r ${NINJAURI_DIR}/requirements.txt
RUN chown -R ninjauri:ninjauri /usr/local/lib/python3.5/site-packages/tldextract

COPY ninjauri.sh ${NINJAURI_DIR}

USER ninjauri
WORKDIR /home/ninjauri

# Run NinjaUri
ENTRYPOINT ["/opt/NinjaUri/ninjauri.sh"]
CMD ["ninjauri.py", "-h"]
