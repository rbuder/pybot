FROM rackspacedot/python37
RUN pip install --upgrade pip
COPY . /pybot
WORKDIR /pybot
RUN ["wget", "https://github.com/grafana/loki/releases/download/v0.4.0/promtail-linux-amd64.gz"]
RUN ["gunzip", "promtail-linux-amd64.gz"]
RUN ["chmod", "+x", "promtail-linux-amd64"]
RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["chmod", "+x", "start.sh"]
ENTRYPOINT ["./start.sh"]
