
FROM ubuntu:22.10

RUN apt-get update -y \
        && apt-get install -y --no-install-recommends \
                python3=3.10.4-0ubuntu2 \
                git=1:2.36.1-1ubuntu1 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*
COPY *.py /usr/bin/
COPY *.sh /usr/bin/
RUN mkdir -p /home/root/workdir/
WORKDIR /home/root/workdir/
