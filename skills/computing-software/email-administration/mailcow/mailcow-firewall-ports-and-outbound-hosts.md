---
id: computing-software.email-administration.mailcow.mailcow-firewall-ports-and-outbound-hosts
name: mailcow-firewall-ports-and-outbound-hosts
category: computing-software
field: email-administration
product: mailcow
tags: [firewall, ports, docker-user-chain, outbound-connections, smtp-ports, imap-ports, bind-address, hetzner-firewall]
level: practitioner
status: docs-checked
description: "Open the right inbound ports, bind services to specific IPs, filter via the DOCKER-USER chain, and allow the outbound hosts mailcow needs."
sources: ["https://docs.mailcow.email/getstarted/prerequisite-system/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow firewall, ports and outbound hosts

Check that the default ports are free with `ss -tlpn | grep -E -w '25|80|110|143|443|465|587|993|995|4190'`. Inbound: SMTP 25, SMTPS 465, submission 587 (postfix-mailcow); IMAP 143, IMAPS 993, POP3 110, POP3S 995, ManageSieve 4190 (dovecot-mailcow); HTTP 80 and HTTPS 443 (nginx-mailcow). Each has a variable in `mailcow.conf` such as `SMTP_PORT`, `IMAPS_PORT`, `HTTP_PORT`.

To bind a service to one address, prefix it: `SMTP_PORT=1.2.3.4:25`. This does not work for `HTTP_PORT` and `HTTPS_PORT`; use `HTTP_PORT=1234` together with `HTTP_BIND=1.2.3.4`.

Firewalld and ufw conflict with Docker's own rules. The docs advise disabling them and putting your ruleset in the `DOCKER-USER` chain, which a Docker restart does not clear. Because mailcow is containerised, INPUT rules do not restrict it; use the FORWARD path instead.

Outbound access needed includes rsync.sanesecurity.net (ClamAV signatures, TCP 873), github.com and hub.docker.com (updates and images), asn-check.mailcow.email (bad ASN checks), fuzzy.mailcow.email and fuzzy1/fuzzy2.rspamd.com (fuzzy hash servers, UDP 11445 and 11335), abuse.ch hosts for malware lists, any host on 25/465 for mail, and DNS (53 TCP and UDP) plus ICMP to public resolvers for Unbound.

With a static firewall such as Hetzner Robot, allow destination ports 1024-65535 for TCP (ack flag) and UDP, because Unbound uses that range for outgoing queries. To narrow it, set `outgoing-port-avoid: 0-32767` in `data/conf/unbound/unbound.conf` and allow 32768-65535.

## Checked

2026-11-04. Confirmed on the Prepare your system page: the port check, inbound port and variable table, the SMTP_PORT=IP:port form and the HTTP_PORT/HTTP_BIND exception, the firewalld/ufw warning with the DOCKER-USER and FORWARD advice, the outbound hosts table (including ports 873, 11445, 11335 and the abuse.ch hosts), and the Hetzner Robot 1024-65535 rules with outgoing-port-avoid. No changes needed.

Method: documentation only; no commands were run.
