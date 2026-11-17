---
id: computing-software.email-administration.mailcow.mailcow-crowdsec-integration
name: mailcow-crowdsec-integration
category: computing-software
field: email-administration
product: mailcow
tags: [crowdsec, firewall-bouncer, ipset, acquis-yaml, allowlist, country-rules]
level: advanced
status: docs-checked
description: "Add CrowdSec log analysis and host firewall bans to mailcow with the community Mailcow-Crowdsec override, including allowlists and bouncer setup."
sources: ["https://docs.mailcow.email/third_party/crowdsec/third_party-crowdsec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CrowdSec integration for mailcow

Mailcow-Crowdsec is a community-maintained project that adds CrowdSec to mailcow through `docker-compose.override.yml`. It reads Docker logs of Postfix, Dovecot and Nginx with CrowdSec collections plus extra local parsers and scenarios, and enforces bans with an iptables/ipset firewall bouncer in the host's INPUT, FORWARD and DOCKER-USER chains. It includes configurable country-based SMTP authentication rules (the supplied ones distinguish Germany `DE` from other countries), repeat-offender scenarios and trusted IP/CIDR allowlists. Enrollment in the CrowdSec Console is optional.

Requirements: Linux host, Docker Compose v2, root or sudo. The bouncer Dockerfile downloads an amd64 binary, so check architecture compatibility.

Setup outline:
1. Copy the project's `crowdsec/` directory and compose override into the mailcow directory, merging `services:` and `volumes:` if an override exists.
2. Adjust container names in `crowdsec/acquis.yaml`.
3. Review `crowdsec/parsers/s02-enrich/whitelists.yaml` and add admin, VPN and monitoring addresses before enabling bans.
4. Review the SMTP scenarios in `crowdsec/scenarios/` and adapt rules and thresholds.
5. Start CrowdSec and check acquisition metrics show all three log sources.
6. Register the firewall bouncer and put its API key in `crowdsec/cs-firewall-bouncer.yaml` (copied from the `.example`).
7. Build and start `cs-firewall-bouncer`, then verify registration, chains and decisions.

The bouncer uses host networking and `NET_ADMIN`, so review host access and ban rules first.

## Checked

2026-11-09. Confirmed on the CrowdSec page: community-maintained override project, log sources, iptables and ipset bouncer chains, country rules for DE, allowlists, optional Console enrollment, requirements and the amd64 bouncer note, the seven setup steps, and the host networking and NET_ADMIN warning. No changes needed.

Method: docs-checked 2026-11-09 against the full CrowdSec page (third_party-crowdsec.en.md in mailcow-dockerized-docs); the external project repository was not read.
