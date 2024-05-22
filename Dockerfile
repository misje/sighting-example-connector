FROM python:3.11-alpine
ENV CONNECTOR_TYPE=INTERNAL_ENRICHMENT

COPY requirements.txt /opt/sighting-example-connector/
WORKDIR /opt/sighting-example-connector
RUN apk --no-cache add build-base libmagic && \
   pip3 install --no-cache-dir -r requirements.txt && \
   apk del build-base
RUN pip3 install --no-cache-dir -r requirements.txt
COPY sighting-enrichment-example.py /opt/sighting-example-connector
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
