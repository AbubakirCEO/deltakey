#!/bin/bash
if [ ! -f delta-bypass ]; then
  wget -q -O delta-bypass https://github.com/AbabaHnb/Delta-Bypass-for-Rust/releases/download/v1.3.0/delta-bypass-v1.3.0-linux-musl-amd64
  chmod +x delta-bypass
fi

nohup ./delta-bypass --serve --host 127.0.0.1 --port 2233 > bypass.log 2>&1 &

python server.py
