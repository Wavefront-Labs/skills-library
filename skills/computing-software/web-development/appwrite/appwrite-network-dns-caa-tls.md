---
id: computing-software.web-development.appwrite.appwrite-network-dns-caa-tls
name: appwrite-network-dns-caa-tls
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, network, dns, caa, tls, custom-domains]
level: advanced
status: docs-checked
description: "Add the CAA record Appwrite Cloud needs, use Appwrite DNS nameservers and avoid third-party cookie problems with custom domains."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/caa-records/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/dns/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/tls/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/custom-domains/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get certificates and cookies working on custom domains.

CAA: Appwrite Cloud issues certificates through Certainly. You only need to act if your domain already has CAA records that lack `certainly.com`; then add a record allowing the issuer value `certainly.com` and keep your existing CAA records. If you use Appwrite DNS, the CAA record is applied for you.

DNS service: Appwrite offers nameservers `ns1.appwrite.zone` and `ns2.appwrite.zone`. An apex domain is connected either by NS records pointing to them or by CNAME flattening.

TLS: connections support TLS 1.2 and 1.3 with certificates provisioned and renewed automatically.

Cookies and custom endpoints: browsers increasingly block third-party cookies. For reliable cookie sessions, use an endpoint on your own domain, such as `appwrite.my-app.com`.

Gotcha: do not replace existing CAA records; add `certainly.com` alongside them.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/network/caa-records, products/network/dns, products/network/tls, products/network/custom-domains. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the Brotli/Gzip/Zstd, DDoS and WAF line and the X-Fallback-Cookies header sentence (not on the cited pages); CAA is only needed when the domain already has CAA records without certainly.com, and Appwrite DNS applies it automatically; apex wording changed to NS records or CNAME flattening; Gotcha reworded; removed Verify.

Method: documentation only; no commands were run.
