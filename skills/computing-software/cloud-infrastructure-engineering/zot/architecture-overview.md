---
id: computing-software.cloud-infrastructure-engineering.zot.architecture-overview
name: architecture-overview
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, architecture, minimal-build, oci-layout, project-overview]
level: intro
status: docs-checked
description: "What Zot is and how it is built: OCI-native registry, minimal versus full builds, search database, scheduler, OCI layout storage, companion tools."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/general/architecture.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/general/concepts.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/general/glossary.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot is a production-ready, vendor-neutral OCI container image registry server: OCI Distribution Spec on the wire and OCI Image Layout on disk. It is Apache 2.0 licensed and a CNCF Sandbox project, and fully conforms to the Distribution Spec.

Structure:
- Single binary, one config file with `http`, `storage`, `log` and `extension` sections.
- Minimal build: core spec only, fewer dependencies, smaller attack surface. Full build: minimal plus extensions, selectable at build and run time.
- Authentication and authorization run before requests reach storage.
- With `search` enabled, zot maintains a database to answer complex queries efficiently via GraphQL; without it, basic queries run against storage and are slower and more limited.
- A scheduler runs GC, sync mirroring and scrub in the background without disturbing foreground API requests.
- OCI Image Layout is the only supported layout; Zot can serve any OCI layout. Deduplication needs hard-link support; remote storage is AWS S3 or an S3-compatible system.
- Trivy performs vulnerability scanning with periodic database updates.

Companion tools: `zli` (CLI), `zb` (benchmark), `zui` (web UI), `zxp` (metrics exporter for minimal images).

Supports cosign and notation signatures; artifacts such as Helm charts can be stored alongside images. Delete by tag is supported.

## Checked

Architecture and concepts pages read. Dropped the MetaDB name, the GCS and Azure cross-reference and the Helm-chart support wording.

Method: docs-checked 2026-11-09 against zot docs general/architecture.md, general/concepts.md and general/glossary.md.
