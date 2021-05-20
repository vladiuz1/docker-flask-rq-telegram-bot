FROM nginx:1.17.4-alpine

RUN rm /etc/nginx/conf.d/default.conf

#RUN /bin/sh -c 'echo "Hello $HOSTNAME"'
#RUN /bin/sh -c 'echo "Hello $ROOT_HOSTNAME"'
#RUN  apk add --no-cache nginx-mod-http-lua
#COPY nginx.conf /etc/nginx/conf.d

COPY nginx.conf.template /etc/nginx/conf.d/nginx.conf.template

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
