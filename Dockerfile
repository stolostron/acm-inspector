
FROM quay.io/openshift/origin-cli:4.22 as builder
FROM registry.access.redhat.com/ubi8/ubi-minimal:latest

RUN microdnf update -y \
    && microdnf install -y tar rsync findutils gzip iproute util-linux python39-pip \
    && microdnf clean all

# Copy oc binary
COPY --from=builder /usr/bin/oc /usr/bin/oc

COPY /src/supervisor/requirements.txt ./

# Upgrade pip to get better wheel support
RUN pip3 install --no-cache-dir --upgrade pip

# Prefer binary wheels to avoid compilation
RUN pip3 install --no-cache-dir --prefer-binary -r requirements.txt

RUN mkdir acm-inspector

COPY . /acm-inspector/

WORKDIR /

CMD [ "/bin/bash", "/acm-inspector/src/supervisor/helper.sh" ]