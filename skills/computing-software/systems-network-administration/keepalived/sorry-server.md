---
id: computing-software.systems-network-administration.keepalived.sorry-server
name: sorry-server
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, sorry-server, virtual-server, fallback, high-availability]
level: practitioner
status: docs-checked
description: "sorry_server adds a fallback server to the pool when every real server is down; syntax and the 192.168.100.100 port 80 example."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sorry_server

`sorry_server @IP PORT` inside a virtual_server names a server that is added to the pool when all real servers are down.

```
virtual_server 192.168.200.15 80 {
    ...
    sorry_server 192.168.100.100 80
}
```
In the case study only the HTTP service has one, serving as the fallback when the pool is unavailable; the SSL and SMTP services have none.

Typical content for it is a maintenance page, but the page does not say what to serve.

Verify: stop all real servers for the service and confirm the sorry server answers on the VIP.

## Checked

2026-11-04. Confirmed the keyword and its meaning on the configuration synopsis page, and the 192.168.100.100 port 80 example and HTTP-only use on the Healthcheck case study page. Nothing removed.

Method: documentation only; no commands were run.
