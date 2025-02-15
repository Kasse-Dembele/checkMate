FROM python:3.7-slim

RUN apt-get update
RUN apt-get -y install jq

COPY pr_checkmate_bot.py entrypoint.sh /action/

RUN pip3 install requests pyyaml

ENTRYPOINT ["/action/entrypoint.sh"]
