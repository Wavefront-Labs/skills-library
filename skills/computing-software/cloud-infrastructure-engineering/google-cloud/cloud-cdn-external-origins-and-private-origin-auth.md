---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-cdn-external-origins-and-private-origin-auth
name: cloud-cdn-external-origins-and-private-origin-auth
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-cdn, external-origin, private-origin-auth, internet-neg, s3-origin]
level: advanced
status: docs-checked
description: "Put Cloud CDN in front of origins outside Google Cloud with internet NEGs, set Host headers, and authenticate to private S3-compatible buckets with AWS v4 private origin auth."
sources: ["https://cloud.google.com/cdn/docs/ext-backend-internet-neg-overview", "https://cloud.google.com/cdn/docs/setting-up-cdn-with-ex-backend-internet-neg", "https://cloud.google.com/cdn/docs/configure-private-origin-authentication", "https://cloud.google.com/sdk/gcloud/reference/compute/backend-services/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud CDN external origins and private origin auth

## 1. Internet NEG for the external origin
```bash
gcloud compute network-endpoint-groups create ext-origin --global \
  --network-endpoint-type=INTERNET_FQDN_PORT
gcloud compute network-endpoint-groups update ext-origin --global \
  --add-endpoint="fqdn=origin.example.net,port=443"
gcloud compute backend-services create ext-be --global --load-balancing-scheme=EXTERNAL_MANAGED \
  --protocol=HTTPS --enable-cdn --cache-mode=CACHE_ALL_STATIC
gcloud compute backend-services add-backend ext-be --global --network-endpoint-group=ext-origin --global-network-endpoint-group
gcloud compute backend-services update ext-be --global --custom-request-header='Host: origin.example.net'
```
- Use INTERNET_FQDN_PORT (an FQDN resolved through public DNS) rather than an IP so origin address changes do not affect the configuration; if the origin expects a particular Host header, set it with `--custom-request-header`, otherwise the client's Host header is preserved.
- Allowlist the Google front-end ranges published in the DNS TXT record `_cloud-eoips.googleusercontent.com` (query it with `dig TXT`).

## 2. Private origin authentication (S3-compatible)
For a private AWS S3 (or other SigV4-compatible) bucket, or a private Cloud Storage bucket with an HMAC key, the backend signs origin requests with an access key. Create an HMAC key tied to a service account first; private origin authentication supports only GET, HEAD, OPTIONS and TRACE.
```bash
gcloud compute backend-services update ext-be --global \
  --security-settings-aws-v4-access-key-id=ACCESS_KEY_ID \
  --security-settings-aws-v4-access-key=ACCESS_KEY \
  --security-settings-aws-v4-access-key-version=KEY_VERSION \
  --security-settings-aws-v4-origin-region=us-east-1
```
Alternatively export the backend with `gcloud compute backend-services export`, add `securitySettings.awsV4Authentication` (`accessKeyId`, `accessKey`, optional `accessKeyVersion`, `originRegion`) to the YAML, and import it again. Set the `Host` header to the value the object store expects.

## Gotchas
- `--cache-key-include-host` controls whether requests to different hosts are cached separately; when several hostnames front one origin, leave it off to avoid duplicate cache entries.
- Use a key version name for each rotation and update the backend with the new key before revoking the old one.

## Verify
- [ ] A request through `https://cdn.example.com/obj` returns 200 and later requests are served from cache (load balancer log `statusDetails` `response_from_cache`); direct anonymous access to the bucket is denied.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: `gcloud compute backend-services update --aws-v4-authentication=...` does not exist; the update reference lists `--security-settings-aws-v4-access-key-id`, `--security-settings-aws-v4-access-key`, `--security-settings-aws-v4-access-key-version` and `--security-settings-aws-v4-origin-region`. The private origin authentication page also documents the YAML route through `backend-services export` and import, and the GET, HEAD, OPTIONS and TRACE restriction.
- Confirmed (external backends and setup pages): internet NEG with INTERNET_FQDN_PORT, `network-endpoint-groups update --add-endpoint="fqdn=...,port=443" --global`, `backend-services add-backend --network-endpoint-group --global-network-endpoint-group`, `--custom-request-header "Host: ..."`, allowlist from the _cloud-eoips.googleusercontent.com TXT record.
- Removed: the one-endpoint-per-NEG and health-check-unsupported statements, the S3 redirect and style remarks, and the egress-cost remark (not found in the pages read).

Method: documentation only; no commands were run.
