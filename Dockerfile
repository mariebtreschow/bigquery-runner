FROM python:3

ARG APP_DIR=/app

RUN set -eux \
    mkdir -p ${APP_DIR}

WORKDIR ${APP_DIR}
COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS "key-file.json"
ENV LOGGING_LEVEL "DEBUG"

RUN apt-get update && apt-get install -y python3-pip \
    && pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "bin/bigquery_runner.py" ]