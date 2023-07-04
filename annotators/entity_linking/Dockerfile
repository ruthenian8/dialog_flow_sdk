FROM tensorflow/tensorflow:1.15.2-gpu

RUN apt-key del 7fa2af80  && \
    rm -f /etc/apt/sources.list.d/cuda*.list && \
    curl https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb \
    -o cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb
RUN apt-get -y update
RUN apt-get install -y build-essential zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm \
    libncurses5-dev libncursesw5-dev xz-utils libffi-dev liblzma-dev

RUN apt-get -y update && \
    apt-get install -y software-properties-common && \
    apt-get update && apt-get install -y git

RUN apt-get install -y sqlite3

ARG CONFIG
ARG COMMIT=0.13.0
ARG PORT
ARG SRC_DIR
ARG SED_ARG=" | "

ENV LANGUAGE "EN"
ENV CONFIG=$CONFIG
ENV PORT=$PORT

COPY ./annotators/entity_linking/requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

RUN mkdir -p /root/.deeppavlov/downloads/wikidata_eng
RUN wget -q -P /root/.deeppavlov/downloads/wikidata_eng http://files.deeppavlov.ai/kbqa/wikidata/kbqa_entity_linking_eng.tar.gz
RUN tar -C /root/.deeppavlov/downloads/wikidata_eng -xvf /root/.deeppavlov/downloads/wikidata_eng/kbqa_entity_linking_eng.tar.gz

RUN pip install git+https://github.com/deepmipt/DeepPavlov.git@${COMMIT}

COPY $SRC_DIR /src

WORKDIR /src

RUN python -m deeppavlov install $CONFIG

RUN sed -i "s|$SED_ARG|g" "$CONFIG"

CMD gunicorn  --workers=1 --timeout 500 server:app -b 0.0.0.0:8075
