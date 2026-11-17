---
id: computing-software.systems-network-administration.keepalived.ssl-get-check
name: ssl-get-check
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, ssl-get, health-checking, https, digest, genhash]
level: practitioner
status: docs-checked
description: "SSL_GET checker: the HTTP_GET structure carried over SSL, with url path and digest, used as the alternative to TCP_CHECK for an HTTPS virtual server."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
  - https://keepalived.readthedocs.io/en/latest/software_design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSL_GET

Same structure and keywords as HTTP_GET (repeatable `url` blocks with `path` and `digest`, plus `connect_port`, `connect_timeout`, `retry`, `delay_before_retry`), but the request goes over SSL. The healthcheck case study offers it as an alternative to TCP_CHECK on the port 443 virtual server, using the same URLs and digests as the HTTP example.

genhash has a `-S` / `--use-ssl` option for connecting to the server with SSL, which is the relevant one when generating digests for this check. The `virtualhost` keyword on the virtual_server applies to HTTP_GET and SSL_GET.

Verify: the digest from genhash -S matches the digest in the url block.

## Checked

2026-11-04. Confirmed SSL_GET keywords on the configuration synopsis page, the SSL_GET example and alternative to TCP_CHECK on the Healthcheck case study page, and the description of SSL_GET and genhash -S on the Software Design and programs synopsis pages. Nothing removed.

Method: documentation only; no commands were run.
