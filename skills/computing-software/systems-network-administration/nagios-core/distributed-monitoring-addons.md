---
id: computing-software.systems-network-administration.nagios-core.distributed-monitoring-addons
name: distributed-monitoring-addons
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, distributed-monitoring, nrpe, nsca, nrdp, ncpa, ndoutils, redundant-monitoring, send-nsca, addons]
level: practitioner
status: docs-checked
description: "What the Nagios Core add-ons do (NRPE, NSCA, NRDP, NCPA, NDOUtils) and how they fit distributed, redundant and failover monitoring; where the docs defer."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/addons.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/distributed.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/redundancy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add-ons and distributed monitoring

| Add-on | Role |
|---|---|
| NRPE | run plugins on remote Linux/Unix hosts (disk, CPU, memory). check_by_ssh can do similar but can impose a higher CPU load on the monitoring machine, especially with hundreds or thousands of hosts |
| NSCA | `send_nsca` on remote hosts submits passive results to a daemon on the Nagios server; suits distributed and failover |
| NRDP | HTTP(S) transport for results and commands, standard ports, optional SSL via Apache, multi-line output, better performance than NSCA |
| NCPA | cross-platform agent with check API and web GUI; active checks via `check_ncpa.py`, passive via NRDP |
| NDOUtils | store all Core status in MySQL; many instances can feed one DB |

More community add-ons live on Nagios Exchange.

## Design
The Core distributed page is only an overview: choose a design by goals and deployment effort; no single solution fits. Options with strengths and weaknesses are in the Distributed Monitoring topics area of the Nagios Core Library; its starting document is titled "Distributed Monitoring Solutions For Nagios Core". Redundant and failover documentation was likewise moved to the Nagios Library.

## Building blocks in Core
Passive checks (`computing-software.systems-network-administration.nagios-core.passive-checks`) and `translate_passive_host_checks` (`computing-software.systems-network-administration.nagios-core.passive-host-state-translation`). Obsess options `obsess_over_services`, `ocsp_command` (default off) run a command after each service check.

## Checked

2026-11-04. Confirmed against the Add-ons, Distributed Monitoring and Redundant and Failover pages (add-on roles, NCPA check_ncpa.py and NRDP, NRDP advantages over NSCA, NDOUtils MySQL, library pointers) and the main configuration page (obsess_over_services default 0, ocsp_command). Reworded the check_by_ssh cost to what the page says and removed the freshness-check mention.

Method: documentation only; no commands were run.
