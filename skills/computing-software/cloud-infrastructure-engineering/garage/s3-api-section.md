---
id: computing-software.cloud-infrastructure-engineering.garage.s3-api-section
name: s3-api-section
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [s3-api, s3-region, root-domain, vhost-style]
level: practitioner
status: docs-checked
description: "Configure [s3_api] bind address, region, vhost-style root_domain and public_endpoint."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `[s3_api]` section keys:

- `api_bind_addr`: IP and port for S3 calls. It does not support TLS, so put a reverse proxy in front. A path can be given instead (since v0.8.5) to create a unix socket with mode 0222.
- `s3_region`: Garage accepts calls targeted at this region. Calls aimed at another region fail with an `AuthorizationHeaderMalformed` error that redirects the client to the right region.
- `root_domain`: optional suffix enabling vhost-style access. With `s3.example.com`, bucket `my-bucket` answers on `my-bucket.s3.example.com`. Path-style requests always work. Vhost-style needs a wildcard DNS entry and possibly a wildcard TLS certificate.
- `public_endpoint`: the full URI (with `http://` or `https://`) clients should use. If unset, the admin API's GetNodeInfo reports no endpoint, and Garage guesses object URLs from `root_domain` when it must return one.
- `public_endpoint_path_style`: whether advertised URLs are path-style; reported by GetNodeInfo. If undefined and `root_domain` is unset it defaults to true.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format. Confirmed on the configuration page: every key of the `[s3_api]` section as described, including the unix socket mode 0222 since v0.8.5, the `AuthorizationHeaderMalformed` error, vhost-style requirements, and the `public_endpoint_path_style` default. No changes needed.

Method: documentation only; no commands were run.
