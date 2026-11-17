---
id: computing-software.web-development.ghost.ghost-nginx-proxy-and-upload-size
name: ghost-nginx-proxy-and-upload-size
category: computing-software
field: web-development
product: ghost
tags: [ghost, nginx, reverse-proxy, x-forwarded-proto, redirect-loop, client-max-body-size]
level: practitioner
status: docs-checked
description: "Fix Ghost redirect loops behind a proxy with X-Forwarded-Proto and raise NGINX client_max_body_size for uploads."
sources:
  - https://github.com/TryGhost/docs/blob/main/faq/proxying-https-infinite-loops.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/image-upload-issues.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Ghost behind your own proxy without loops or failed uploads.

Ghost-CLI's NGINX template proxies to `http://127.0.0.1:2368` and sets headers:

```
location / {
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header Host $http_host;
  proxy_pass http://127.0.0.1:2368;
}
client_max_body_size 50m;
```

Infinite HTTPS redirect loop: when a proxy (NGINX, Apache, CloudFront, any other) terminates SSL and talks to Ghost over http, Ghost thinks requests are insecure and redirects to https forever. Set the `X-Forwarded-Proto` header to `https` so Ghost knows the original request was secure.

Upload failures: image uploads can be affected by the default max upload size of 50mb. For large images, themes or imports raise `client_max_body_size`. Log into the server, go to the Ghost installation folder (the guide uses `/var/www/ghost`), edit `system/files/<your-domain>.conf`, set `client_max_body_size {VALUE}M;`, save, and restart NGINX with `sudo service nginx restart`.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): faq/proxying-https-infinite-loops.mdx (24 lines) and faq/image-upload-issues.mdx (15 lines). The config block, loop explanation and upload steps match. Removed as unconfirmed: the advice that Ghost's configured `url` must use https and the Verify step with `curl -I`.
Method: documentation only; no commands were run.
