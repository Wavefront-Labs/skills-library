---
id: computing-software.cybersecurity-defensive.trivy.self-host-trivy-databases
name: self-host-trivy-databases
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [self-hosting, oras, crane, regclient, media-types, manual-cache-population, vex-hub-mirror]
level: sme
status: docs-checked
description: "Mirror trivy-db, trivy-java-db and trivy-checks into your registry or populate the cache by hand, and serve a private copy of VEX Hub."
sources:
  - https://trivy.dev/latest/docs/guide/advanced/self-hosting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OCI route: copy `trivy-db`, `trivy-java-db` and `trivy-checks` with any registry tool (crane, ORAS, regclient), keep them updated, and point Trivy at the copies with `--db-repository`, `--java-db-repository` and `--checks-bundle-repository`. Registry credentials follow the private registry authentication rules. If you proxy or manipulate the images, note the non-standard layer media types: `application/vnd.aquasec.trivy.db.layer.v1.tar+gzip` (trivy-db), `application/vnd.aquasec.trivy.javadb.layer.v1.tar+gzip` (trivy-java-db) and `application/vnd.oci.image.manifest.v1+json` (trivy-checks).

Manual cache population: on a connected machine run `oras pull ghcr.io/aquasecurity/trivy-db:2` and `tar -xzf db.tar.gz`, or `trivy image --cache-dir . --download-db-only`. You get `trivy.db` and `metadata.json`; copy them into `<cache dir>/db/` on the isolated host (find the cache dir with `trivy -h | grep cache`). For the Java DB use `ghcr.io/aquasecurity/trivy-java-db:1`, archive `javadb.tar.gz`, files `trivy-java.db` and `metadata.json`, subdirectory `java-db`.

VEX Hub copy: download `main.zip` of the vexhub repository and its `vex-repository.json` manifest, edit the manifest location `url` to your server's zip URL, serve the manifest under `/.well-known/vex-repository.json`, run `trivy vex repo init`, set the default repo `enabled: false` and add your server as a custom repository.

## Checked

2026-11-03. Read and confirmed against the Self-Hosting page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
