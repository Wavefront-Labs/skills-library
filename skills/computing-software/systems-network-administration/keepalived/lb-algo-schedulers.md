---
id: computing-software.systems-network-administration.keepalived.lb-algo-schedulers
name: lb-algo-schedulers
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, lb-algo, scheduler, ipvs, round-robin, least-connection, hashing]
level: practitioner
status: docs-checked
description: "IPVS schedulers: the lb_algo keywords listed in the configuration synopsis (rr, wrr, lc, wlc, sh, dh, lblc) and the ten algorithm names in the scheduling page."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/scheduling_algorithms.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schedulers (lb_algo)

The synopsis gives these keywords: `rr`, `wrr`, `lc`, `wlc`, `sh`, `dh`, `lblc`.

The scheduling-algorithms page lists ten IPVS algorithms by name only (its section bodies carry no further text in the fetched version):
1. Round Robin
2. Weighted Round Robin
3. Least Connection
4. Weighted Least Connection
5. Locality-Based Least Connection
6. Locality-Based Least Connection with Replication
7. Destination Hashing
8. Source Hashing
9. Shortest Expected Delay
10. Never Queue

Case-study picks: wrr for HTTP (with weights 2 and 1), rr for SSL, wlc for SMTP.

The keywords for the names beyond those in the synopsis are not given on the fetched pages, so check them in the configuration reference for your version before using them.

## Checked

2026-11-04: lb_algo keywords confirmed in the configuration synopsis; the ten names in the Scheduling Algorithms page; case-study picks in the healthcheck and mixing case studies. Removed the Verify line.
Method: documentation only; no commands were run.
