---
id: computing-software.systems-network-administration.keepalived.http-get-check
name: http-get-check
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, http-get, health-checking, url, digest, retry, delay-before-retry]
level: practitioner
status: docs-checked
description: "HTTP_GET checker: repeatable url blocks with path and MD5 digest, plus connect_timeout, retry and delay_before_retry; example with two URLs on one real server."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP_GET

Fetches each listed URL and compares the MD5 digest of the response with the expected value.

```
real_server 192.168.100.2 80 {
    weight 2
    HTTP_GET {
        url {
            path /testurl/test.jsp
            digest ec90a42b99ea9a2f5ecbe213ac9eba03
        }
        url {
            path /testurl2/test.jsp
            digest 640205b7b0fc66c1ea91c463fac6334c
        }
        connect_timeout 3
        retry 3
        delay_before_retry 2
    }
}
```
- `url { path ... digest ... }`: repeatable.
- `connect_port`: port to test.
- `connect_timeout`, `retry` (maximum retries), `delay_before_retry`: numeric.
- `virtualhost` on the virtual_server names the HTTP virtual host used for HTTP_GET and SSL_GET.

Produce digests with genhash.

Verify: change the page content and the real server drops from the pool.

## Checked

2026-11-04. Confirmed the url, path, digest, connect_port, connect_timeout, retry and delay_before_retry keywords and the two-URL example on the configuration synopsis and Healthcheck case study pages, and the MD5 digest comparison on the Software Design page. Reworded the virtualhost line to match the synopsis.

Method: documentation only; no commands were run.
