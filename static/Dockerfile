FROM nginx:1.17-alpine

RUN apk add bash

RUN mkdir /config

COPY templates/* /etc/nginx/conf.d/
COPY conf/* /etc/nginx/conf/
