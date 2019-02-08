FROM python:3
WORKDIR /usr/src/farmbot-py
RUN pip install paho-mqtt
RUN pip install requests
ENV PYTHONPATH=/usr/src/farmbot-py/src
ADD . .
ENTRYPOINT [ "python", "./src/farmbot/garden_bed.py" ]