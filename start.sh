#!/usr/bin/env sh

if [ "$VERBOSE" = "true" ]; then
    python main.py --loglevel=$LOGLEVEL --verbose > pybot.log 2> pybot.error.log &
else
    python main.py --loglevel=$LOGLEVEL > pybot.log 2> pybot.error.log &
fi

sed -i -e "s/loki:3100/${LOKIURL}:${LOKIPORT}/g" promtail.yaml

./promtail-linux-amd64 -config.file promtail.yaml