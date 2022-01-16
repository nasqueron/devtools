FROM debian:11

RUN apt update && apt install -y python3 python3-requests \
    --no-install-recommends && rm -r /var/lib/apt/lists/*

COPY github /opt/github

WORKDIR /opt

CMD "/bin/bash"
