### What's this?

Simple Telegram bot for the NAS

### Requirements
```
python3
a Telegram bot
```

### Usage

```
virtualenv -p python3 venv
pip install -r requirements.txt
update config.yml with your token
python main.py
```

### Docker Usage

```
docker run -it --rm -e TOKEN=YOURTOKENHERE ronaldbuder/pybot
```

or

```
git clone https://github.com/rbuder/pybot.git
cd pybot
docker build -t hubuser/containername .
docker run -it --rm -e TOKEN=YOURTOKENHERE hubuser/containername
```