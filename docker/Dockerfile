FROM python:3.12-alpine

ENV NINJAURI_HOME=/opt/NinjaUri
ENV NINJAURI_USER=ninjauri

# Install general dependencies
RUN apk update && apk upgrade
RUN pip install pipenv

# Install NinjaUri

RUN adduser -Ds /bin/sh ${NINJAURI_USER} \
    && mkdir -p ${NINJAURI_HOME}

COPY Pipfile ${NINJAURI_HOME}/Pipfile
COPY Pipfile.lock ${NINJAURI_HOME}/Pipfile.lock
COPY ninjauri.py ${NINJAURI_HOME}

# NOTE: To install only production dependencies remove the "--dev" flag from the below "pipenv install" command!
#RUN PIPENV_PIPFILE=${NINJAURI_HOME}/Pipfile pipenv install --system --deploy \
RUN PIPENV_PIPFILE=${NINJAURI_HOME}/Pipfile pipenv install --dev --system --deploy \
    && chown -R ninjauri:ninjauri /usr/local/lib/python3.12/site-packages/tldextract \
    && ln -s ${NINJAURI_HOME}/ninjauri.py /usr/local/bin/ninjauri

USER ninjauri
WORKDIR /home/ninjauri

# Run NinjaUri

CMD ["ninjauri", "-h"]
