---
id: computing-software.cloud-infrastructure-engineering.external-dns.pdns-provider-domain-filter
name: pdns-provider-domain-filter
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, pdns-provider, powerdns-api, pdns-server-id, domain-filter-parent-zones]
level: practitioner
status: docs-checked
description: "Configure the ExternalDNS PowerDNS provider: required flags, existing-zones assumption, leading-dot and parent-zone domain-filter behaviour, regex filter and API verification."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/pdns.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerDNS provider

Needs PowerDNS Auth Server 4.1.x or later and ExternalDNS v0.5 or later. The zones must already exist and be configured; the provider does not add, remove or configure zones. Dry-run is not supported.

```yaml
args:
- --source=service
- --policy=upsert-only
- --provider=pdns
- --pdns-server={{ pdns-api-url }}
- --pdns-server-id={{ pdns-server-id }}
- --pdns-api-key={{ pdns-http-api-key }}
- --txt-owner-id={{ owner-id-for-this-external-dns }}
- --domain-filter=external-dns-test.my-org.com
- --interval=30s
```

**Domain filter semantics (zones)**
- `--domain-filter=example.org` allows zone `example.org` and zones ending in `.example.org`.
- `--domain-filter=.example.org` allows only zones ending in `.example.org`, not `example.org` itself.
- `--domain-filter=a.example.com` can match the parent zone `example.com`; with a leading dot, parent zones are not matched.
- `--regex-domain-filter` overrides domain filters and can be given once.

**CNAME to ALIAS:** see the alias annotation skill; PowerDNS can serve ALIAS with `expand-alias`.

**Verify:** wait one interval, then
```bash
curl -H "X-API-Key: ${PDNS_API_KEY}" ${PDNS_API_URL}/api/v1/servers/localhost/zones/example.com. | jq '.rrsets[] | select(.name | contains("echo"))'
dig @${PDNS_FQDN} echo.example.com.
```
Do not `dig` before the record exists: negative caching (RFC 2308) is hard to flush.

**Local test:** run `powerdns/pdns-auth-49` in Docker with `--api=yes --api-key=secret --zone-cache-refresh-interval=0` and external-dns `--once`; `--publish-internal-services` publishes a ClusterIP.

## Checked

2026-11-04. Confirmed against the ExternalDNS PowerDNS tutorial (prerequisites, feature support, deployment args, domain filter and regex filter behaviour, verification steps, local Docker test) and the annotations page (PowerDNS alias with expand-alias). Nothing removed.
Method: documentation only; no commands were run.
