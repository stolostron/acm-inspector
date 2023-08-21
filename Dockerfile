#https://hub.docker.com/r/amd64/python/
FROM python:3.9-bookworm

COPY /src/supervisor/requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir acm-inspector

COPY . /acm-inspector/

# refer https://www.ibm.com/docs/en/guardium-insights/3.2.x?topic=azure-install-openshift-command-line-interface-cli
RUN mkdir /ocp-tools
RUN wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable-4.13/openshift-client-linux.tar.gz -P /ocp-tools
WORKDIR /ocp-tools
RUN chmod 777 /ocp-tools
RUN tar xvf openshift-client-linux.tar.gz oc kubectl
RUN rm openshift-client-linux.tar.gz
RUN cp oc /usr/local/bin
RUN cp kubectl /usr/local/bin

WORKDIR /

#CMD [ "python", "/src/supervisor/entry.py" ]
CMD [ "/bin/bash", "/acm-inspector/src/supervisor/helper.sh" ]