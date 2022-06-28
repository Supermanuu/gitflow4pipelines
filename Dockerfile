
FROM ubuntu:22.10

RUN apt-get update -y \
        && apt-get install -y --no-install-recommends \
                python3=3.10.4-0ubuntu2 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
COPY *.py /usr/bin/
RUN mkdir -p /home/root/workdir/
WORKDIR /home/root/workdir/
