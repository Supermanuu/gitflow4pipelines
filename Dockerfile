
FROM ubuntu:focal

RUN apt-get update -y \
        && apt-get install -y --no-install-recommends \
                python3=3.8.2-0ubuntu2 \
                git=1:2.25.1-1ubuntu3.4 \
                ssh=1:8.2p1-4ubuntu0.5 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Scripts
COPY *.py /usr/bin/
COPY *.sh /usr/bin/

# Working dir
RUN mkdir -p /home/root/workdir/
WORKDIR /home/root/workdir/

# Adding workdir to git safe list
RUN git config --global --add safe.directory /home/root/workdir

# Disabling host ssh fingerprint checking
COPY avoidHostKeyCheking.conf /etc/ssh/ssh_config.d/
