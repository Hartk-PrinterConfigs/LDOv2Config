#!/bin/bash
echo $(curl 192.168.1.16/server/history/list?limit=1&start=0&since=1&before=5&order=asc)
