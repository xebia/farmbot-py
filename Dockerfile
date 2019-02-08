FROM python:3
WORKDIR /usr/src/farmbot-py
ADD . .
RUN pip install paho-mqtt
RUN pip install requests
ENV PYTHONPATH=/usr/src/farmbot-py/src
#ENTRYPOINT [ "python", "./farmbot/garden_bed.py" ]