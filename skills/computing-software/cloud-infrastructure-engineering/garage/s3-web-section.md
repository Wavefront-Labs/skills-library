---
id: computing-software.cloud-infrastructure-engineering.garage.s3-web-section
name: s3-web-section
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [s3-web, website-root-domain, add-host-to-metrics, static-website]
level: practitioner
status: docs-checked
description: "Configure the [s3_web] website endpoint, its root_domain and host-label metrics."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `[s3_web]` section controls publishing bucket content as websites.

- `bind_addr`: IP and port accepting HTTP requests for website-enabled buckets. No TLS is supported, so use a reverse proxy; a unix socket path is possible since v0.8.5.
- `root_domain`: optional suffix appended to a bucket name to form the HTTP Host. With `web.example.com`, a bucket named `deuxfleurs.fr` is reachable as `deuxfleurs.fr.web.example.com` or simply `deuxfleurs.fr`. If unset, the bucket name must equal the requested hostname.
- `add_host_to_metrics`: whether to put the requested Host header in the Prometheus metrics of the web endpoint. It is off by default because the number of possible values is unbounded and can cause cardinality explosion.

The Quick Start's example configuration also sets `index = "index.html"` in this section; the configuration reference page does not list that key.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Quick Start. Confirmed on the configuration page: `bind_addr` (no TLS, unix socket since v0.8.5), `root_domain` with its example, and `add_host_to_metrics` with the cardinality reason. Confirmed on the Quick Start: the `index` key in the example. Removed: the paragraph about the website guide (serving rules, global alias, `garage bucket website --allow`), which is not on any cited page.

Method: documentation only; no commands were run.
