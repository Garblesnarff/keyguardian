FROM nginx:1.27-alpine

RUN apk add --no-cache bash

COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template
COPY 10-envsubst.sh /docker-entrypoint.d/10-envsubst.sh
RUN chmod +x /docker-entrypoint.d/10-envsubst.sh

EXPOSE 80 443


