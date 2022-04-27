# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
ENV DECISION_MAKER_JAR_URL=https://github.com/ldss-hse/ldss-core-aggregator/releases/download/decision_maker_v0.4/lingvo-dss-all.jar
ENV JAVA_PATH=/opt/java
ENV JDK_URL=https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
ENV VIRTUAL_ENV=$WORKING_DIRECTORY/venv
ENV WORKING_DIRECTORY=/api
ENV FLASK_ENV=production

ENV PATH=$PATH:${JAVA_PATH}/jdk-17.0.2/bin

RUN apt --yes update && \
    apt --yes upgrade && \
    apt install --yes curl

RUN mkdir ${JAVA_PATH}

RUN curl $JDK_URL | tar -xz -C ${JAVA_PATH}

COPY requirements.txt api/requirements.txt
COPY requirements_dev.txt api/requirements_dev.txt

WORKDIR /api

RUN python3 -m pip install virtualenv
RUN python3 -m virtualenv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt

ENV PYTHONPATH="$WORKING_DIRECTORY/core_api:$PYTHONPATH"

RUN echo $PATH
RUN echo $PYTHONPATH

RUN java --version

COPY core_api/ core_api/
RUN curl -L $DECISION_MAKER_JAR_URL \
            -o core_api/core_api/async_tasks/decision_maker/scripts/bin/lingvo-dss-all.jar

CMD [ "python", "core_api/core_api/app.py"]
