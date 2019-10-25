FROM rackspacedot/python37
RUN pip install --upgrade pip
COPY . /pybot
WORKDIR /pybot
RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["chmod", "+x", "start.sh"]
ENTRYPOINT ["./start.sh", "$TOKEN"]
