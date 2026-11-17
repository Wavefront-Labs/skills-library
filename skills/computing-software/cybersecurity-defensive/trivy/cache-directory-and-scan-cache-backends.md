---
id: computing-software.cybersecurity-defensive.trivy.cache-directory-and-scan-cache-backends
name: cache-directory-and-scan-cache-backends
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [cache-dir, cache-backend, redis, boltdb, trivy-clean, cache-ttl, redis-tls]
level: advanced
status: docs-checked
description: "Control Trivy's cache directory, clear it with trivy clean, and pick the fs, memory or Redis scan cache backend, including Redis TLS flags."
sources:
  - https://trivy.dev/latest/docs/guide/configuration/cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The cache holds previous scan results (scan cache), the vulnerability DB, the Java index DB, misconfiguration checks and VEX repositories. Cache options apply to every scanner.

Clear it with `trivy clean`: `--scan-cache` removes scan results, `--vuln-db` removes the vulnerability database, and `--all` removes everything. Choose the location with `--cache-dir`:

```bash
trivy --cache-dir /tmp/trivy/ image python:3.4-alpine3.9
```

The scan cache backend is experimental and set with `--cache-backend`:
- `fs` (local file system): default for container image, VM image and repository scans, and uses `--cache-dir`. It is built on BoltDB, so only one process can use the cache at a time; a second process is locked out.
- `memory`: results are discarded when the process ends; default for filesystem and SBOM scans, and usable for images: `trivy image debian:11 --cache-backend memory`.
- `redis://[HOST]:[PORT]`: share the cache between Trivy instances, with `--cache-ttl` for expiry.

Redis examples:
```bash
trivy server --cache-backend redis://localhost:6379 --redis-tls
trivy server --cache-backend redis://localhost:6379 \
  --redis-ca /path/to/ca-cert.pem --redis-cert /path/to/cert.pem --redis-key /path/to/key.pem
```

## Checked

2026-11-03. Read and confirmed against the Cache page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
