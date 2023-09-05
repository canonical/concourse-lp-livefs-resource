FROM ubuntu:jammy-20230816
RUN apt-get update && apt-get install -y python3 python3-requests python3-requests-oauthlib python3-launchpadlib
ADD /check /out /in /lputils.py /opt/resource/
RUN chmod +x /opt/resource/*
