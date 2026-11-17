---
id: computing-software.devops-ci-cd.verdaccio.url-prefix-and-public-url
name: url-prefix-and-public-url
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [url-prefix, public-url, subpath, url-prefix-setting, verdaccio-public-url, sub-directory]
level: practitioner
status: docs-checked
description: "Serve Verdaccio under a sub-path or fixed public URL behind a proxy with url_prefix and VERDACCIO_PUBLIC_URL, and how they combine."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/reverse-proxy/
  - https://verdaccio.org/docs/env/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`url_prefix` is for servers behind a reverse proxy; forms `/verdaccio`, `verdaccio/` and `verdaccio` all become `/verdaccio/`.

```yaml
url_prefix: /verdaccio/
```
`VERDACCIO_PUBLIC_URL` sets the public base: used for web UI assets (js, favicon), for the dist base in returned metadata, and it ignores the `Host` and `X-Forwarded-Proto` headers. A defined `url_prefix` is appended:

```
VERDACCIO_PUBLIC_URL='https://somedomain.org'   url_prefix: '/my_prefix'  ->  https://somedomain.org/my_prefix/
VERDACCIO_PUBLIC_URL='https://somedomain.org'   url_prefix: '/'          ->  https://somedomain.org/
VERDACCIO_PUBLIC_URL='https://somedomain.org/first_prefix'  url_prefix: '/second_prefix'  ->  https://somedomain.org/second_prefix/
```
Proxy rules from the reverse proxy page:
- If the whole domain is Verdaccio, do not set `url_prefix`; send `Host $host:$server_port` and `X-Forwarded-Proto $scheme`.
- For a sub-directory (`location ~ ^/verdaccio/(.*)$` proxying to `http://127.0.0.1:4873/$1`), set `url_prefix: /verdaccio/` with the trailing slash.

Symptom of missing Host header: assets served as relative `http://127.0.0.1:4873/-/static`. Verify by loading the UI and checking that the dist URLs in the returned package metadata use the public URL.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (URL Prefix), Reverse Proxy and Environment Variables. Confirmed: the url_prefix normalisation, VERDACCIO_PUBLIC_URL behaviour and the three combination examples, the proxy rules and the relative static asset symptom. Removed or corrected: the npm view command in the verify line.

Method: documentation only; no commands were run.
