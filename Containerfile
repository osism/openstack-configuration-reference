FROM ubuntu:24.04

ARG VERSION=wallaby

COPY main.py /main.py
COPY namespaces.yaml /namespaces.yaml
COPY requirements.txt /requirements.txt
COPY templates /templates

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        apt-transport-https \
        python3-pip \
        software-properties-common \
    && add-apt-repository cloud-archive:${VERSION} \
    && apt-get install --no-install-recommends -y \
        python3-barbican \
        python3-ceilometer \
        python3-cinder \
        python3-glance \
        python3-keystone \
        python3-neutron \
    && pip3 install --no-cache-dir -r /requirements.txt \
    && mkdir /output \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf \
      /var/cache/apt \
      /var/lib/apt/lists/* \
      /root/.cache \
      /tmp/* \
      /usr/share/doc/* \
      /usr/share/man/* \
      /var/tmp/*
