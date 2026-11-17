---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.security-toml-jwt-and-grpc-tls
name: security-toml-jwt-and-grpc-tls
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [security-toml, jwt-signing, grpc-mtls, grpc-tls]
level: advanced
status: docs-checked
description: "Secure a SeaweedFS cluster with security.toml: JWT signing for volume writes and reads, gRPC mTLS, HTTPS, UI exposure and search path."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration
  - https://github.com/seaweedfs/seaweedfs/wiki/Security-Overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# security toml jwt and grpc tls

Generate the template: `weed scaffold -config=security`. It is read from `./security.toml`, `$HOME/.seaweedfs/security.toml`, then `/etc/seaweedfs/security.toml`, by master, volume and filer.

Key sections:
- `[jwt.signing]` `key`, `expires_after_seconds` (default 10): the master issues write JWTs, volume servers validate. Setting a key disables the volume UI unless `[access] ui = true`.
- `[jwt.signing.read]`: same for reads (master plus volume setups only).
- `[jwt.filer_signing]` and `[jwt.filer_signing.read]`: filer HTTP JWTs.
- `[grpc]` `ca`, with `[grpc.volume]`, `[grpc.master]`, `[grpc.filer]`, `[grpc.s3]`, `[grpc.client]` cert/key for mTLS.
- `[https.client]`, `[https.volume]`, `[https.master]`, `[https.filer]` for the HTTP data plane.
- `[cors.allowed_origins]`, `[filer.expose_directory_metadata]`, `[s3.trusted_proxies]`.

Two layers need securing separately: gRPC (control plane: heartbeats, metadata) and HTTP(S) (data plane: uploads and downloads).

Keep secrets out of the file with `WEED_` environment variables (dots become underscores).

Gotcha: if the filer is publicly reachable without read JWT, disable directory metadata exposure.

Verify: with the key set, a write to a volume server without a JWT is rejected.

## Checked
Checked 2026-11-09: the scaffold command and search path, the JWT sections with the 10 second default, the volume UI disable and `[access] ui`, the gRPC and HTTPS sections, the two-layer split, `WEED_` environment overrides and the directory-metadata warning all match the pages. Nothing removed.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Security-Configuration and Security-Overview, both read in full from a local clone of the wiki.
