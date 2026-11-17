---
id: computing-software.systems-network-administration.headscale.magicdns-base-domain
name: magicdns-base-domain
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, magicdns, base-domain, override-local-dns, dns-certificates]
level: practitioner
status: docs-checked
description: "Configure Headscale MagicDNS: magic_dns, base_domain rules, override_local_dns, and optional DNS certificates through a DNS challenge provider."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/dns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MagicDNS and base domain

Headscale supports most Tailscale DNS features; settings live under `dns`.

```yaml
dns:
  magic_dns: true
  base_domain: example.com
  override_local_dns: true
```

- `base_domain` MUST differ from the `server_url` domain.
- `override_local_dns: true` (default) forces Headscale's DNS configuration over the node's local settings.
- MagicDNS also serves extra records (dns-extra-records).

## DNS certificates (optional)

```yaml
dns:
  certificates:
    enabled: false
```

Lets nodes get certificates for MagicDNS names with `tailscale cert`; requires a DNS challenge provider. Related keys: `certificates.zone` (defaults to `base_domain`), `challenge.propagation_timeout: 2m` (0 disables the check), `challenge.resolvers` (defaults to 1.1.1.1 and 8.8.8.8), `challenge.provider` (acmedns, cloudflare, gigahost, hetzner, powerdns or rfc2136).

## Verify

On a client: `tailscale dns status --all`.

## Checked

2026-11-04. Confirmed against config-example.yaml and the Headscale DNS page: magic_dns, base_domain rule (must differ from the server_url domain), override_local_dns default, dns.certificates, zone, propagation_timeout 2m, resolvers default, and the provider list.
Method: documentation only; no commands were run.
