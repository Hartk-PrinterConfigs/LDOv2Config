#!/bin/bash
tar -cz --sort=name --exclude='printer-????????_??????.cfg'
    -C /home/pi/klipper_config/config/ . | \
curl --data-binary @- \
    -H 'Authorization: Token c84c641e597b9a6e5e3471b61771e8f899dd5994' \
    https://dev.vorondb.com/api/printer/7/config/