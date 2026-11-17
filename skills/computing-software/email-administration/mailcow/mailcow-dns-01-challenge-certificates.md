---
id: computing-software.email-administration.mailcow.mailcow-dns-01-challenge-certificates
name: mailcow-dns-01-challenge-certificates
category: computing-software
field: email-administration
product: mailcow
tags: [dns-01, acme-dns-challenge, wildcard-certificate, acme-sh, dns-provider-api]
level: advanced
status: docs-checked
description: "Switch acme-mailcow to the DNS-01 challenge (mailcow 2026-03 or later) for wildcard certificates or servers without public port 80."
sources: ["https://docs.mailcow.email/post_installation/firststeps-ssl-dns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Certificates with the DNS-01 challenge

DNS-01 proves domain ownership through a TXT record at `_acme-challenge.<domain>` that mailcow creates through your DNS provider's API using acme.sh, which supports over 150 providers. Use it for wildcard certificates (`*.example.com`), servers whose port 80 is blocked, complex reverse proxy setups, or several servers sharing a domain. Stay with the default HTTP-01 for simple single-server setups, or when your DNS provider has no API.

Requires mailcow 2026-03 or later, API credentials with permission to edit DNS records, and a provider supported by acme.sh.

Configuration:
1. In `mailcow.conf` set `ACME_DNS_CHALLENGE=y`, `ACME_DNS_PROVIDER=<plugin>` (for example `dns_cf` for Cloudflare, `dns_aws` for Route 53, `dns_servercow`, `dns_ionos`, `dns_ovh`) and `ACME_ACCOUNT_EMAIL`.
2. Put the provider's credential variables in `data/conf/acme/dns-01.conf` (for Servercow, `SERVERCOW_API_Username` and `SERVERCOW_API_Password`).
3. Apply with `docker compose up -d` so acme-mailcow restarts.

Notes: with DNS-01 enabled `SKIP_HTTP_VERIFICATION` is implied and port 80 is not needed. All domains in the installation use DNS-01; HTTP-01 and DNS-01 cannot be mixed. Credential variable names per provider follow the acme.sh DNS API wiki. For Hetzner, domains in the new Hetzner Console use `dns_hetznercloud` with `HETZNER_TOKEN`; domains in the legacy DNS Console use `dns_hetzner` with `HETZNER_Token`. A wildcard `*.example.com` does not cover `example.com` itself, so set `ADDITIONAL_SAN=*.example.com,example.com`.

## Checked

2026-11-04. Confirmed on the DNS-01 page: the 2026-03 requirement, acme.sh with over 150 providers, when to use or avoid DNS-01, ACME_DNS_CHALLENGE, ACME_DNS_PROVIDER, ACME_ACCOUNT_EMAIL, data/conf/acme/dns-01.conf, the Servercow variables, the docker compose up -d step, SKIP_HTTP_VERIFICATION implied, no mixing of HTTP-01 and DNS-01, and the plugin names dns_cf, dns_aws, dns_servercow, dns_ionos, dns_ovh. Fixed: Hetzner needs dns_hetznercloud or dns_hetzner depending on console, added the wildcard apex limitation.

Method: documentation only; no commands were run.
