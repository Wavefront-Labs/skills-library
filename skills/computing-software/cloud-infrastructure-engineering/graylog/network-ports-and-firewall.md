---
id: computing-software.cloud-infrastructure-engineering.graylog.network-ports-and-firewall
name: network-ports-and-firewall
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [firewall, ports, outbound-urls, air-gapped, network]
level: practitioner
status: docs-checked
description: "Graylog server-to-server ports and outbound connectivity needed for firewalls and air-gapped deployments."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/network_connectivity_and_firewall_requirements.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# network ports and firewall

Default server-side ports (may vary by configuration):
- Graylog to Data Node/OpenSearch: 9200 TCP (search and indexing)
- Graylog to Data Node: 8999 TCP (management, coordination, health)
- Graylog to MongoDB: 27017 TCP
- Browser to Graylog: 9000 TCP (web interface and REST API)

Outbound from the Graylog server, and effect if blocked:
- `https://contenthub.graylog.cloud/` and `https://glc-illuminate-hub.s3.amazonaws.com/`: Illuminate packs must be uploaded manually.
- `https://versioncheck.graylog.com/check`: no update notifications.
- `https://api.graylog.com`: standard licenses with remote checks eventually become invalid.
- `https://packages.graylog2.org/`: no package installs or upgrades.
- `https://downloads.graylog.org/`: no manual downloads.

Some endpoints use CloudFront, so `*.cloudfront.net` may be needed. Browser-side features can work if the user's workstation has internet even when servers do not.

## Checked

2026-11-04. Confirmed against the Network Connectivity and Firewall Requirements page (ports table, outbound endpoints and behaviour if blocked, CloudFront hint, browser-side note). The page lists further MongoDB-host and browser endpoints not repeated here.

Method: documentation only; no commands were run.
