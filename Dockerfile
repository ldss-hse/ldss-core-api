# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
ENV WORKING_DIRECTORY=/api
ENV VIRTUAL_ENV=$WORKING_DIRECTORY/venv

ENV PATH=$PATH:/opt/java/jdk-17.0.2/bin

COPY build.sh .

RUN  apt  --yes update &&  apt --yes upgrade && apt install --yes curl
RUN chmod +x build.sh && \
    ./build.sh

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

CMD [ "python", "core_api/core_api/app.py"]
