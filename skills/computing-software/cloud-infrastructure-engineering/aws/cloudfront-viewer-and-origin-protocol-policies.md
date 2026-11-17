---
id: computing-software.cloud-infrastructure-engineering.aws.cloudfront-viewer-and-origin-protocol-policies
name: cloudfront-viewer-and-origin-protocol-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudfront, viewer-protocol-policy, origin-protocol-policy, tls-security-policy, https]
level: practitioner
status: docs-checked
description: "Set CloudFront viewer protocol policy, origin protocol policy and TLS security policies, and fix 502s from origin certificate and protocol mismatches."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https-viewers-to-cloudfront.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https-cloudfront-to-custom-origin.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/secure-connections-supported-viewer-protocols-ciphers.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Viewer and origin protocol policies, TLS settings

## 1. Viewer side (per cache behavior)
| `ViewerProtocolPolicy` | Effect |
|---|---|
| `allow-all` | HTTP and HTTPS served |
| `redirect-to-https` | GET and HEAD get 301 to HTTPS; POST, PUT, DELETE, OPTIONS and PATCH over HTTP 1.1+ get 307, and below HTTP 1.1 get 403 |
| `https-only` | HTTP gets 403 |
Distribution `ViewerCertificate`: an ACM certificate must be requested or imported in us-east-1, `SSLSupportMethod: sni-only` (recommended; `vip` is not recommended and costs extra), and a `MinimumProtocolVersion` security policy. API values include `TLSv1.2_2021`, `TLSv1.2_2025` and `TLSv1.3_2025`; the supported-protocols table in the CloudFront guide shows which TLS versions and ciphers each policy allows. HTTP redirects are billed as two requests.

## 2. Origin side (custom origins)
```json
"CustomOriginConfig":{"OriginProtocolPolicy":"https-only","HTTPSPort":443,
  "OriginSslProtocols":{"Quantity":1,"Items":["TLSv1.2"]},
  "OriginReadTimeout":30,"OriginKeepaliveTimeout":5}
```
| Policy | Use |
|---|---|
| `https-only` | CloudFront always uses HTTPS to the origin |
| `http-only` | S3 **website** endpoints, which do not support HTTPS |
| `match-viewer` | origin protocol follows the viewer's; use it only with viewer policy redirect-to-https or https-only |

## 3. 502 checklist
- The certificate returned by the origin must include the origin domain name or, if the Host header is forwarded, the Host header domain. For an ELB origin you can use an ACM certificate; other origins need a certificate from a CA on the Mozilla list. Self-signed certificates are not accepted.
- If the origin returns an expired, invalid or self-signed certificate, a wrong-order chain, or a chain missing intermediates, CloudFront drops the connection and returns 502 with `X-Cache: Error from cloudfront`.
- Also confirm the origin supports a TLS version listed in `OriginSslProtocols` (API values `SSLv3`, `TLSv1`, `TLSv1.1`, `TLSv1.2`).
- `OriginReadTimeout` is 1-120 seconds (default 30) and `OriginKeepaliveTimeout` 1-120 seconds (default 5) in the API documentation.

## 4. Apply
`aws cloudfront get-distribution-config --id E123 > d.json`, edit `.DistributionConfig`, then
`aws cloudfront update-distribution --id E123 --if-match <ETag> --distribution-config file://cfg.json`.

## Verify
- [ ] `curl -sI http://d123.cloudfront.net/` returns 301 to https.
- [ ] A TLS handshake with a version your security policy excludes fails, and one it includes succeeds.

## Checked
2026-10-27. Documentation: Amazon CloudFront Developer Guide (HTTPS between viewers and CloudFront, HTTPS to custom origins, supported protocols and ciphers, CNAME and HTTPS requirements) plus CloudFront API model documentation for viewer certificate and custom origin settings, read this date. Confirmed: redirect and 403 behaviours (including 307 for non-GET methods, which the draft omitted), match-viewer guidance, ACM in us-east-1, sni-only recommendation, 502 conditions for bad origin certificates, S3 website endpoints lack HTTPS, timeouts and defaults, enum values. Removed the claim that TLSv1.2_2021 removes weak ciphers (see the protocol table instead).
Method: documentation only; no commands were run.
