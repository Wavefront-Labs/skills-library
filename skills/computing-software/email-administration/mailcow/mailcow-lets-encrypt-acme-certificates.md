---
id: computing-software.email-administration.mailcow.mailcow-lets-encrypt-acme-certificates
name: mailcow-lets-encrypt-acme-certificates
category: computing-software
field: email-administration
product: mailcow
tags: [lets-encrypt, acme-mailcow, additional-san, force-renew, skip-ip-check, skip-http-verification, additional-server-names]
level: practitioner
status: docs-checked
description: "How acme-mailcow obtains certificates for the hostname and autodiscover names, adds SANs, forces renewal and handles validation failures."
sources: ["https://docs.mailcow.email/post_installation/firststeps-ssl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Let's Encrypt certificates in mailcow

The `acme-mailcow` container requests a certificate for `MAILCOW_HOSTNAME` and, for each added mail domain, for `autodiscover.<domain>` and `autoconfig.<domain>` if they resolve to the server (IPv6 first, else IPv4). Only names that validate become SANs, and removing a domain moves the certificate aside and requests a new one. Port 80 must reach mailcow for the HTTP-01 challenge. Wildcards or firewalled port 80 call for the DNS-01 method instead. Any external ACME client such as certbot also works if it places the files correctly.

Extra names: set `ADDITIONAL_SAN` in `mailcow.conf` with no quotes and no spaces, for example `ADDITIONAL_SAN=smtp.*,cert1.example.com`. With HTTP-01, `smtp.*` creates `smtp.<domain>` for each mailcow domain. To use such a name to open the web UI, also list it in `ADDITIONAL_SERVER_NAMES` (comma separated, no spaces). Recreate the affected containers with `docker compose up -d` afterwards.

Force renewal: `touch data/assets/ssl/force_renew` in the mailcow directory, run `docker compose restart acme-mailcow`, and watch the acme-mailcow logs; the file is deleted automatically.

Validation problems: `SKIP_IP_CHECK=y` skips the IP check (useful for multi-IP setups but a misconfiguration can get you rate-limited by Let's Encrypt). If IP validation passes but HTTP validation fails, a firewall such as firewalld or ufw is probably blocking traffic from `br-mailcow` to the external interface. `SKIP_HTTP_VERIFICATION=y` skips that check but is discouraged. Re-apply after changing a SKIP_* setting.

## Checked

2026-11-04. Confirmed on the Advanced SSL page: certificate names requested (hostname, autodiscover and autoconfig), IPv6-then-IPv4 resolution, validated-only SANs, port 80 requirement, DNS-01 pointer, ADDITIONAL_SAN format and smtp.* behaviour, ADDITIONAL_SERVER_NAMES, SKIP_IP_CHECK, the firewalld/ufw br-mailcow explanation, and SKIP_HTTP_VERIFICATION. Fixed: forcing renewal also needs a restart of acme-mailcow.

Method: documentation only; no commands were run.
