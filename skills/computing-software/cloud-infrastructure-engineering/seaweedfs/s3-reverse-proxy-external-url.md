---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-reverse-proxy-external-url
name: s3-reverse-proxy-external-url
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [nginx, externalurl, x-forwarded-host, reverse-proxy, trusted-proxies]
level: practitioner
status: docs-checked
description: "Put nginx or another proxy in front of SeaweedFS S3: forwarded headers, virtual-hosted buckets, -s3.externalUrl for SigV4, trusted proxies for aws:SourceIp."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Nginx-Proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 reverse proxy external url

SigV4 signs the `Host` header, so the host SeaweedFS sees must match what the client signed.

Option 1, forward headers: set `X-Forwarded-Host` (and `X-Forwarded-Port` for non-standard ports). SeaweedFS combines them. Virtual-hosted bucket URLs need a wildcard DNS record for the S3 subdomain.

Option 2, pin the external URL (ignores incoming `Host` and `X-Forwarded-*`):
```bash
weed s3 -s3.externalUrl=https://s3.example.com:9000
weed mini -s3.externalUrl=http://localhost:9000
weed filer -s3 -s3.externalUrl=https://s3.mycorp.internal
# or
export WEED_S3_EXTERNAL_URL=https://s3.example.com:9000
```
Source IP policies: `X-Forwarded-For` / `X-Real-IP` count toward `aws:SourceIp` only for trusted proxies. In `security.toml`:
```toml
[s3.trusted_proxies]
white_list = "10.10.10.0/24"
```
When the proxy strips a URL path prefix such as `/s3`, send `X-Forwarded-Prefix` with that prefix. Standard ports (80, 443) are omitted from the reconstructed host automatically.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 Nginx Proxy: SigV4 Host signing, X-Forwarded-Host and Port, wildcard DNS for virtual-hosted buckets, `-s3.externalUrl` and `WEED_S3_EXTERNAL_URL`, trusted proxies white_list, X-Forwarded-Prefix. Removed the 'undefined AWS behavior' wording and the Verify line (neither is on this page).
Method: documentation only; no commands were run.
