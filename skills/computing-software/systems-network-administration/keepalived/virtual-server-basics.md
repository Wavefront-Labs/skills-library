---
id: computing-software.systems-network-administration.keepalived.virtual-server-basics
name: virtual-server-basics
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, virtual-server, lvs, ipvs, delay-loop, lb-algo, lb-kind, protocol, fwmark]
level: practitioner
status: docs-checked
description: "virtual_server block keywords: address and port or fwmark, delay_loop, lb_algo, lb_kind, protocol TCP or UDP, with the HTTP example from the healthcheck case study."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# virtual_server

Declared as `virtual_server (@IP PORT)|(fwmark num) { ... }`.

```
virtual_server 192.168.200.15 80 {
    delay_loop 30
    lb_algo wrr
    lb_kind NAT
    persistence_timeout 50
    protocol TCP
    sorry_server 192.168.100.100 80
    real_server ... { ... }
}
```
- `delay_loop`: seconds between health checks.
- `lb_algo`: scheduler (rr, wrr, lc, wlc, sh, dh, lblc per the synopsis).
- `lb_kind`: NAT, DR or TUN.
- `protocol`: TCP or UDP.
- `virtualhost`: HTTP virtual host for HTTP_GET or SSL_GET.
- `fwmark`: makes it a firewall-mark service instead of address plus port.
- `nat_mask`: obsolete unless using LVS on Linux 2.2 kernels.

The page documents no defaults for these keywords.

Verify: the IPVS table lists the virtual service with the configured scheduler and its real servers.

## Checked

2026-11-04. Confirmed the virtual_server synopsis, keyword list, scheduler and forwarding values, and the nat_mask note on the configuration synopsis page, and the HTTP example on the Healthcheck case study page. Nothing removed.

Method: documentation only; no commands were run.
