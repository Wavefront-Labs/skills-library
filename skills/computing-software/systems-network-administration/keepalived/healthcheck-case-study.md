---
id: computing-software.systems-network-administration.keepalived.healthcheck-case-study
name: healthcheck-case-study
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, case-study, healthcheck, lvs, nat, virtual-server, smtp]
level: advanced
status: docs-checked
description: "Healthcheck case study: NAT LVS router with HTTP, SSL and SMTP virtual services on 192.168.200.15, scheduler, persistence and check settings per service."
sources:
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Healthcheck case study

A NAT-based LVS router (often in a DMZ) owns the load-balanced range and runs Keepalived from /etc/keepalived/keepalived.conf. Base LVS and system setup is assumed done.

| Service | Port | delay_loop | lb_algo | persistence_timeout | Checker |
|---|---|---|---|---|---|
| HTTP | 80 | 30 | wrr | 50 | HTTP_GET, 2 URLs on server 1 |
| SSL | 443 | 20 | rr | 360 | TCP_CHECK (SSL_GET alternative) |
| SMTP | 25 | 15 | wlc | 50 | TCP_CHECK |

All use `lb_kind NAT`, `protocol TCP`, VIP 192.168.200.15. Real servers 192.168.100.2 and .3 serve HTTP/SSL; .4 and .5 serve SMTP (weights 1 and 2). HTTP uses sorry_server 192.168.100.100 port 80. HTTP_GET uses connect_timeout 3, retry 3, delay_before_retry 2.

global_defs: email recipients, sender, smtp_server 192.168.200.20, smtp_connect_timeout 30, lvs_id LVS_MAIN.

Verify: each service's real servers appear in the IPVS table and drop out when their check fails.

## Checked

2026-11-04. Confirmed against the Case Study: Healthcheck page: the table values, VIP 192.168.200.15, real server addresses and weights, sorry_server, HTTP_GET timers, SMTP server settings and lvs_id. Nothing removed.

Method: documentation only; no commands were run.
