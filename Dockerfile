
FROM quay.io/openshift/origin-cli:4.13 as builder
FROM registry.access.redhat.com/ubi8/ubi-minimal:latest

RUN microdnf update -y \
    && microdnf install -y tar rsync findutils gzip iproute util-linux wget python39-pip \
    && microdnf clean all

RUN wget https://github.com/mikefarah/yq/releases/download/v4.2.0/yq_linux_amd64 -O /usr/bin/yq &&\
    chmod +x /usr/bin/yq
# Copy oc binary
COPY --from=builder /usr/bin/oc /usr/bin/oc

COPY /src/supervisor/requirements.txt ./
RUN pip3 install -r requirements.txt

RUN mkdir acm-inspector

COPY . /acm-inspector/

WORKDIR /

CMD [ "/bin/bash", "/acm-inspector/src/supervisor/helper.sh" ]