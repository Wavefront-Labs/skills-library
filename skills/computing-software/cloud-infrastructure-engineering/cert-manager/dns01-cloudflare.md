---
id: computing-software.cloud-infrastructure-engineering.cert-manager.dns01-cloudflare
name: dns01-cloudflare
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [cloudflare, dns01, api-token, apitokensecretref, apikeysecretref]
level: practitioner
status: docs-checked
description: "Set up cert-manager DNS01 with Cloudflare using a scoped API token (or global key), the required permissions, and the two known error causes."
sources:
  - https://cert-manager.io/docs/configuration/acme/dns01/cloudflare/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
API token (recommended): create under User Profile > API Tokens with permissions `Zone - DNS - Edit` and `Zone - Zone - Read`, Zone Resources `Include - All Zones`.

Secret: name `cloudflare-api-token-secret`, type `Opaque`, `stringData.api-token`.

Issuer, under `spec.acme.solvers[].dns01.cloudflare`:
```yaml
apiTokenSecretRef:
  name: cloudflare-api-token-secret
  key: api-token
```

Global API key (less secure; carries the permissions of your whole account): Secret `cloudflare-api-key-secret` with `stringData.api-key`, and the solver sets `email` (the Cloudflare account email) plus `apiKeySecretRef` with `name` and `key: api-key`.

Troubleshooting:
- Error that the token cannot list zones (`com.cloudflare.api.account.zone.list`): either the token lacks `Zone - Zone - Read`, or cert-manager worked out the wrong zone name because of DNS issues; the docs suggest changing the DNS01 self-check nameservers (`--dns01-recursive-nameservers`).
- `Cloudflare API error for POST "/zones/<id>/dns_records`: Cloudflare blocks API DNS updates for the `.cf`, `.ga`, `.gq`, `.ml` and `.tk` TLDs. Use another DNS provider for those.

For a ClusterIssuer, keep the Secret in the cluster resource namespace (default `cert-manager`).

## Checked

2026-11-03. Confirmed on the cert-manager Cloudflare page (configuration/acme/dns01/cloudflare): token permissions and zone resources, both Secret layouts and field names, the zone list error causes, the blocked TLD list. The ClusterIssuer Secret namespace rule is confirmed on the DNS01 provider pages (CyberArk, ACMEDNS, Route53, CloudDNS) rather than this page. Nothing removed.
Method: documentation only; no commands were run.
