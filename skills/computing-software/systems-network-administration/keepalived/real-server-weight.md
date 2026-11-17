---
id: computing-software.systems-network-administration.keepalived.real-server-weight
name: real-server-weight
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, real-server, weight, virtual-server, wrr, wlc]
level: practitioner
status: docs-checked
description: "real_server @IP PORT block with weight and an attached checker; case-study weights 2 and 1 under wrr and wlc."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# real_server and weight

```
real_server 192.168.100.2 80 {
    weight 2
    HTTP_GET { ... }
}
real_server 192.168.100.3 80 {
    weight 1
    HTTP_GET { ... }
}
```
- `real_server @IP PORT` declares a backend; one health-check block (TCP_CHECK, MISC_CHECK, HTTP_GET or SSL_GET) hangs off it.
- `weight` is its load-balancing weight (numeric). It matters to weighted schedulers such as wrr and wlc.

In the case study the SMTP service uses wlc with weights 1 and 2; the SSL service uses rr with weight 1 each. The prose of that study says SSL weight 2 while the config sets 1, so follow the config you actually intend.

Verify: the IPVS virtual server table lists each real server with its weight.

## Checked

2026-11-04. Confirmed the real_server and weight keywords on the configuration synopsis page and the case-study weights, including the prose and config mismatch for the SSL service, on the Healthcheck case study page. Removed the ipvsadm reference, which neither page mentions.

Method: documentation only; no commands were run.
