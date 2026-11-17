---
id: computing-software.cloud-infrastructure-engineering.external-dns.cloudflare-credentials-and-throttling
name: cloudflare-credentials-and-throttling
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, cloudflare-provider, cf-api-token, zone-id-filter, cloudflare-dns-records-per-page]
level: practitioner
status: docs-checked
description: "Cloudflare provider auth precedence (API token vs key and email), token scopes, zone-id-filter, secret newline trap and the 1,200 per 5 minutes rate limit."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/cloudflare.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloudflare provider: credentials and throttling

**Auth precedence:** `CF_API_TOKEN` wins if set. Otherwise `CF_API_KEY` and `CF_API_EMAIL` are both required. Do not set key and email alongside a token. A token can come from a file: `CF_API_TOKEN="file:/path/to/token"`.

**Token scopes:** Zone `Read`, DNS `Edit`, access to `All zones`. To restrict to specific zones, also pass `--zone-id-filter` so API calls touch only those zones.

**Newline trap:** surrounding whitespace is trimmed as a fallback only. Build the Secret without a trailing newline:
```shell
printf '%s' "$CF_API_TOKEN" | kubectl create secret generic cloudflare-api-key --from-file=apiKey=/dev/stdin
```

**Helm values:**
```yaml
provider:
  name: cloudflare
env:
  - name: CF_API_TOKEN
    valueFrom:
      secretKeyRef:
        name: cloudflare-api-key
        key: apiKey
```

**Throttling:** the Cloudflare API has a global limit of 1,200 requests per five minutes. Several fast-polling ExternalDNS instances in one account can exhaust it. Pass `--cloudflare-dns-records-per-page` with a high value (maximum 5,000). The tutorial also points to the AWS provider throttling section for further recommendations.

**Optional flags in the docs:** `--cloudflare-proxied`, `--cloudflare-regional-services` with `--cloudflare-region-key="eu"`, and `--cloudflare-record-comment` (up to 100 chars on free zones, 500 on paid).

## Checked

2026-11-04. Read the Cloudflare tutorial (Creating Cloudflare Credentials, Throttling, deploy manifests). Confirmed the CF_API_TOKEN precedence, file: syntax, whitespace trimming, the printf secret command, token scopes, --zone-id-filter, the 1,200 per five minutes limit, the 5,000 maximum and the record-comment length limits. Removed the invented AWS-advice parenthetical and the upsert-only-then-sync advice.

Method: documentation only; no commands were run.
