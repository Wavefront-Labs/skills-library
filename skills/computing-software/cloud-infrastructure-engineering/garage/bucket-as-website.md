---
id: computing-software.cloud-infrastructure-engineering.garage.bucket-as-website
name: bucket-as-website
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [website-hosting, garage-bucket-website, index-document, error-document]
level: practitioner
status: docs-checked
description: "Publish a bucket as a static website with garage bucket website --allow and understand the Host matching rules."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/cookbook/exposing-websites/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three ways expose a bucket as a website: the `PutBucketWebsite` S3 call (allowed for keys with the owner bit), the Garage CLI, or the admin API. Garage supports only a subset of the S3 website configuration: index and error documents, no redirections.

From the CLI: `garage bucket website --allow my-website`. It is then public on the web endpoint, port 3902 by default. The bucket needs a global alias; buckets from `garage bucket create` have one, but buckets created through the S3 API need an alias added manually.

Serving rules: static content only, no directory listing, index file per bucket (`--index-document`, default `index.html`), custom 404 document through `--error-document`.

With `root_domain = ".web.example.com"` and a bucket named `garagehq.deuxfleurs.fr`, Garage serves it when Host matches `garagehq.deuxfleurs.fr.web.example.com` or `garagehq.deuxfleurs.fr` (port ignored). Test without DNS: `curl -H 'Host: garagehq.deuxfleurs.fr' http://localhost:3902`.

For production, listen on port 80 (iptables `REDIRECT` to 3902 is suggested) or put a reverse proxy in front for TLS and CORS.

## Checked

2026-11-04. Read the Exposing buckets as websites page in full. Confirmed the three methods, the owner-bit rule, the subset of website configuration, the CLI command, port 3902, the global alias requirement, the serving rules, the Host matching example, the curl test and the port 80 options. Nothing removed.
Method: documentation only; no commands were run.
