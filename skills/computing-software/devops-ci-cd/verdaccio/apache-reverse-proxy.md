---
id: computing-software.devops-ci-cd.verdaccio.apache-reverse-proxy
name: apache-reverse-proxy
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [apache, mod-proxy, allowencodedslashes, nocanon, limitrequestbody]
level: practitioner
status: docs-checked
description: "Proxy Verdaccio with Apache httpd: nocanon and AllowEncodedSlashes NoDecode, SSL virtual host, LimitRequestBody 0 for large publishes, and the gzip checksum fix."
sources:
  - https://verdaccio.org/docs/reverse-proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Apache and mod_proxy must not decode or re-encode slashes.

Root path:
```
<VirtualHost *:80>
  ServerName your.domain.com
  ProxyPreserveHost On
  AllowEncodedSlashes NoDecode
  ProxyPass / http://127.0.0.1:4873/ nocanon
  ProxyPassReverse / http://127.0.0.1:4873/
</VirtualHost>
```
Relative path `/npm`: `ProxyPass /npm http://127.0.0.1:4873 nocanon` and `ProxyPassReverse /npm http://127.0.0.1:4873`.

SSL host (inside `<IfModule mod_ssl.c>`): `SSLEngine on`, `SSLCertificateFile`, `SSLCertificateKeyFile`, `SSLProxyEngine On`, `ProxyRequests Off`, `ProxyPreserveHost On`, `AllowEncodedSlashes NoDecode`, `LimitRequestBody 0`, the nocanon `ProxyPass`, and `RequestHeader set X-Forwarded-Proto "https"`.

Large publishes: `npm publish` of a big tarball failing with `413 Request Entity Too Large` needs `LimitRequestBody 0` (nginx equivalent `client_max_body_size 0;`).

Invalid checksum: `npm WARN tar TAR_ENTRY_INVALID checksum failure` / `zlib: incorrect data check` can come from gzip; add `SetEnv no-gzip 1` to the virtual host only if you see it.

Also set `server.trustProxy`. A runnable httpd:2.4 example is in the Docker examples repository.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Reverse Proxy and Configuration (server.trustProxy section). Confirmed: the root and /npm virtual hosts, the SSL virtual host directives, LimitRequestBody 0 for 413, the gzip checksum fix and the httpd:2.4 Docker example. Removed or corrected: nothing.

Method: documentation only; no commands were run.
