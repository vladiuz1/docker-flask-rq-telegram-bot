#!/usr/bin/env sh

set -eu

envsubst '${NGINX_HOSTNAME} ${NGINX_PORT} ${NGINX_SSL_PORT}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

exec "$@"

