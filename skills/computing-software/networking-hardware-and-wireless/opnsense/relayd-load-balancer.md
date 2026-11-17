---
id: computing-software.networking-hardware-and-wireless.opnsense.relayd-load-balancer
name: relayd-load-balancer
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [relayd, load-balancer, virtual-server, table-check]
level: advanced
status: docs-checked
description: "Build a relayd load balancer on OPNsense with hosts, tables, table checks, virtual servers, protocols and the status page, including an ICMP-checked SMTP example."
sources: ["https://docs.opnsense.org/manual/relayd.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# relayd load balancing

The relayd plugin provides a load balancer for layer 3 or layer 7 forwarding with availability checks of backend servers. Its main advantage is transparent layer-3 redirection, which is lightweight and forwards the unmodified session to the target.

Objects, from bottom up:
- Hosts: the actual targets; basically a unique name and an IP address.
- Tables: lists of hosts acting as a group; one host may be in several tables.
- Table checks: how a group's readiness is decided, such as an icmp ping or requesting a URI and checking the response code. Common checks are installed with the plugin and you can add more.
- Virtual Server: ties it together with bind address and port and a Server Type, either Redirection (firewall, transparent) or Relay (layer 7). Standard mode shows only the primary table plus Scheduler (how traffic is divided) and the check; a backup table is used when all hosts in the primary are down. If the backends listen on a different port than the virtual server, expand advanced settings to set the target port.
- Protocols: templates of TCP options, SSL settings and application-layer rules for relays, visible only in advanced view; see relayd.conf(5).

General settings enable the service, set the host check interval and resource limits. The status page shows the running configuration and offers maintenance actions; filter presets are stored in the browser.

Example: hosts host_1 (10.0.0.1) and host_2 (10.0.0.2), a table named table containing both, and a virtual server ExampleServer of type Redirection on 192.168.1.1 port 25, table table, scheduler Round Robin, table check ICMP. Enable relayd on the general tab and save.

## Checked

2026-11-03. Read the Relayd manual page (relayd.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
