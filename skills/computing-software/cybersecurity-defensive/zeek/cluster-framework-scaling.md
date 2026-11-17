---
id: computing-software.cybersecurity-defensive.zeek.cluster-framework-scaling
name: cluster-framework-scaling
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, cluster-framework, symmetric-hashing, cluster-in-a-box, shunting]
level: practitioner
status: docs-checked
description: "Zeek cluster framework: session affinity via symmetric hashing, proxy count guidance, cluster-in-a-box deployments and shunting."
sources: ["https://docs.zeek.org/en/current/frameworks/cluster.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cluster framework scaling

The premise: split traffic into smaller pieces while keeping each network session on one analysis process. This lets analysis spread over dozens or hundreds of workers, to line speeds of 100G or more.

Components: manager, workers, proxies, and an optional logger. Proxy sizing: for four or fewer workers a single proxy is usually enough; for larger clusters watch proxy CPU and memory and add proxies as needed.

A load-balancing or aggregation device in front must ensure each TCP session reaches a single link, which is done through symmetric hashing. Its output ports feed Zeek nodes on commodity hardware.

Deployments have moved from separate servers per role to cluster-in-a-box: one multi-core machine with dedicated cores hosting workers, proxies, logger and manager. The page cites instances of 90 workers on one physical server. The preferred approach is a load-balancing NIC (Myricom, or Intel with PF_RING or AF_PACKET support) dividing traffic among local workers.

Optional shunting detects large flows by predetermined characteristics and uses an API to make the tap stop sending them to Zeek.

Define nodes in `<prefix>/etc/node.cfg` on the manager: comment out the standalone node and add logger, manager, proxy and worker entries.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
