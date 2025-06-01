#!/usr/bin/env bash

set -euo pipefail

NAME="nginx-dev-proxy"
docker build -t "$NAME" . --no-cache

# Stop and remove the container if it exists
docker stop "$NAME" || true
docker rm "$NAME" || true
docker run -d --name "$NAME" -p 127.0.0.1:80:80 "$NAME"
echo "React app is running with access to API at http://localhost"
