---
id: computing-software.email-administration.mailcow.mailcow-common-problems-and-logs
name: mailcow-common-problems-and-logs
category: computing-software
field: email-administration
product: mailcow
tags: [troubleshooting, unhealthy-container, address-in-use, backup-mx-loop, cannot-send-mail, docker-compose-logs, blacklist-check]
level: practitioner
status: docs-checked
description: "Diagnose frequent mailcow failures such as unhealthy containers, port conflicts, mail loops and sending problems, and read container logs with docker compose."
sources: ["https://docs.mailcow.email/troubleshooting/debug-common_problems/", "https://docs.mailcow.email/troubleshooting/debug-logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow common problems and log reading

Logs (default JSON logging driver only): from the mailcow directory, `docker compose logs` shows all containers; add `--tail=100` to limit lines, `-f` to follow, `-t` for timestamps and `--no-color`; name a service to see just one.

Common problems from the docs:
- Mail loops back to yourself: check whether the domain was set as a backup MX in the mailcow UI.
- Can receive but not send: check whether your IP is on a blacklist, and whether a consumer ISP router blocks mail ports; test reachability of ports 465 or 587 with telnet.
- Mail marked as spam: review the DNS configuration (PTR, SPF, DKIM, DMARC).
- Weird docker compose errors (`Invalid interpolation format`, `'NoneType' object has no attribute 'keys'`, a service named `version`): update Docker and Docker Compose to the latest versions.
- Container XY is unhealthy: a health condition is not met. The most common cause is an updated git clone with an old Docker image, or the reverse; a firewall that blocks traffic on the 172.22.1.1/24 container network can also cause it, as can a wrongly linked file such as the SSL certificate that stops Nginx. Read the logs.
- Address already in use: another program holds one of the mailcow ports; follow the prerequisites firewall and ports section.

## Checked

2026-11-09. Confirmed against the mailcow Common Problems and Logs pages: log options, backup MX loop, blacklist and ISP port checks, compose error messages, unhealthy-container causes including the 172.22.1.1/24 network, and the address-in-use advice. Reworded the unhealthy-container cause to match the page.

Method: docs-checked 2026-11-09 against docs.mailcow.email/troubleshooting/debug-common_problems/ and docs.mailcow.email/troubleshooting/debug-logs/ (whole pages).
