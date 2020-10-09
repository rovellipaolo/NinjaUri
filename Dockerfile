FROM python:3.5-slim-stretch

ENV NINJAURI_HOME=/opt/NinjaUri

RUN useradd -ms /bin/bash ninjauri

# Install dependencies
RUN apt update && \
    apt install -qy python3 python3-pip

# Install NinjaUri
RUN mkdir -p ${NINJAURI_HOME}
COPY requirements.txt ${NINJAURI_HOME}
COPY ninjauri.py ${NINJAURI_HOME}
COPY tests/ ${NINJAURI_HOME}/tests/

RUN pip3 install -r ${NINJAURI_HOME}/requirements.txt
RUN chown -R ninjauri:ninjauri /usr/local/lib/python3.5/site-packages/tldextract

COPY ninjauri.sh ${NINJAURI_HOME}

USER ninjauri
WORKDIR /home/ninjauri

# Run NinjaUri
ENTRYPOINT ["/opt/NinjaUri/ninjauri.sh"]
CMD ["ninjauri.py", "-h"]
