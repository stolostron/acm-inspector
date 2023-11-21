
FROM quay.io/openshift/origin-cli:4.13 as builder
FROM registry.access.redhat.com/ubi8/ubi-minimal:latest

RUN microdnf update -y \
    && microdnf install -y tar rsync findutils gzip iproute util-linux python39-pip \
    && microdnf clean all

# Copy oc binary
COPY --from=builder /usr/bin/oc /usr/bin/oc

COPY /src/supervisor/requirements.txt ./
RUN pip3 install -r requirements.txt

RUN mkdir acm-inspector

COPY . /acm-inspector/

WORKDIR /

CMD [ "/bin/bash", "/acm-inspector/src/supervisor/helper.sh" ]