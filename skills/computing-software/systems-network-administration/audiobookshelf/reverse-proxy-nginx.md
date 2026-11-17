---
id: computing-software.systems-network-administration.audiobookshelf.reverse-proxy-nginx
name: reverse-proxy-nginx
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [reverse-proxy, nginx, websocket, tls, client-max-body-size]
level: practitioner
status: docs-checked
description: "Configure NGINX in front of Audiobookshelf with upgrade headers, forwarded headers and a raised upload size limit."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/1.nginx-proxy-setup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add a server block to your NGINX site config, replacing the placeholders and certificate paths:

```nginx
server {
   listen 443 ssl;
   server_name <sub>.<domain>.<tld>;

   access_log /var/log/nginx/audiobookshelf.access.log;
   error_log /var/log/nginx/audiobookshelf.error.log;

   ssl_certificate      /path/to/certificate;
   ssl_certificate_key  /path/to/key;

   location / {
      proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto  $scheme;
      proxy_set_header Host               $http_host;
      proxy_set_header Upgrade            $http_upgrade;
      proxy_set_header Connection         "upgrade";
      proxy_http_version                  1.1;
      proxy_pass                          http://<URL_to_forward_to>;
      proxy_redirect                      http:// https://;
      client_max_body_size                10240M;
   }
}
```

`client_max_body_size 10240M` prevents the 413 Request Entity Too Large error when uploading large books.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: NGINX reverse proxy page.

Method: documentation only; no commands were run.
