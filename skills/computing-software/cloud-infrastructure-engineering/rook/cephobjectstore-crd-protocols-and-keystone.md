---
id: computing-software.cloud-infrastructure-engineering.rook.cephobjectstore-crd-protocols-and-keystone
name: cephobjectstore-crd-protocols-and-keystone
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [protocols, enableapis, swift, urlprefix, accountinurl, keystone, s3-enabled]
level: advanced
status: docs-checked
description: "Select enabled RGW APIs, Swift URL options and Keystone authentication in a CephObjectStore spec."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Object-Storage/ceph-object-store-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.protocols`:
- `enableAPIs`: the list of RGW APIs to enable, matching `rgw_enable_apis`. Values: s3, s3website, swift, swift_auth, admin, sts, iam, notifications. If empty, all are enabled.
- `s3.enabled`: defaults to true even when the section is absent. S3 should not be disabled in a Ceph multisite configuration. `s3.authUseKeystone` makes S3 also authenticate via Keystone; false uses default S3 auth.
- `swift.accountInUrl`: default false, so the URL is `http://host:port/<rgw_swift_url_prefix>/v1`. When true it is `.../v1/AUTH_<account_name>`, which is required for publicly-readable containers and temporary URLs.
- `swift.urlPrefix`: default `swift`. Setting it to `/` automatically disables the S3 API, because radosgw cannot serve both S3 and Swift with that prefix.
- `swift.versioningEnabled`: enables OpenStack Swift object versioning, so clients can set `X-Versions-Location` on containers.

`spec.auth.keystone` adds an authentication provider; with the page's example, S3 is implicitly enabled even if not listed:
- `url`: the Keystone API endpoint.
- `acceptedRoles`: roles RGW accepts.
- `implicitTenants`: true, false, swift or s3.
- `revocationInterval`: seconds between token revocation checks.
- `tokenCacheSize`: maximum entries in each token cache.
- `serviceUserSecretName`: secret holding the admin user credentials RGW uses toward Keystone.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-object-store-crd) against this skill: 19 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 7 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
