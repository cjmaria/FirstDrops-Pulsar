#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

FROM openjdk:8-jre

ARG pulsar_version=2.4.1

# Install some utilities
RUN apt-get update && \
    apt-get install -y netcat \
                    python \
                    supervisor \
                    postgresql sudo \
                    python-psycopg2 \
                    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /components

# Pulsar
RUN wget https://archive.apache.org/dist/pulsar/pulsar-${pulsar_version}/apache-pulsar-${pulsar_version}-bin.tar.gz && \
    tar xvzf apache-pulsar-${pulsar_version}-bin.tar.gz && \
    mv apache-pulsar-${pulsar_version} /pulsar && \
    rm apache-pulsar-${pulsar_version}-bin.tar.gz


WORKDIR /scripts

### Pulsar dashboard dependencies
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && rm get-pip.py
RUN pip install Django psycopg2 pytz requests
COPY pulsar-dashboard/postgresql.conf /etc/postgresql/9.6/main/

# Configure supervisor
COPY pulsar-dashboard/pulsar-dashboard.conf /etc/supervisor/conf.d/
COPY pulsar-dashboard/django /pulsar/django

# Setup database and create tables
RUN sudo -u postgres /etc/init.d/postgresql start && \
    sudo -u postgres psql --command "CREATE USER docker WITH PASSWORD 'docker';" && \
    sudo -u postgres createdb -O docker pulsar_dashboard && \
    cd /pulsar/django && \
    ./manage.py migrate && \
    sudo -u postgres /etc/init.d/postgresql stop

# Collect all static files needed by Django in a
# single place. Needed to run the app outside the
# Django test web server
RUN cd /pulsar/django && ./manage.py collectstatic --no-input
ENV SERVICE_URL http://localhost:8080/
### end pulsar dashboard

# Function python dependencies
RUN pip install pulsar-client protobuf futures grpcio grpcio-tools

COPY mobius.conf /etc/supervisor/conf.d/
COPY apply-config-from-env.py /pulsar/bin

# Copy examples function jar
COPY firstdrops-pulsar-latest.jar /components/

# Settings for lower memory consumption
ENV PULSAR_MEM ' -Xmx1024M -XX:MaxDirectMemorySize=1024M'
ENV PULSAR_GC ' -XX:+UseG1GC'
ENV managedLedgerCacheSizeMB 32

ENV BOOKIE_MEM ' -Xm1024M -XX:MaxDirectMemorySize=1024M'
ENV BOOKIE_GC ' -XX:+UseG1GC'
ENV dbStorage_writeCacheMaxSizeMb 16
ENV dbStorage_readAheadCacheMaxSizeMb 16
ENV dbStorage_readAheadCacheBatchSize 0
ENV dbStorage_rocksDB_blockCacheSize=16777216
ENV dbStorage_rocksDB_writeBufferSizeMB=8
ENV statsProviderClass org.apache.bookkeeper.stats.PrometheusMetricsProvider
ENV prometheusStatsHttpPort 8001

ENTRYPOINT ["supervisord", "-n"]
