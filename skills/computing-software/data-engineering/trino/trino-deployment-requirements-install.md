---
id: computing-software.data-engineering.trino.trino-deployment-requirements-install
name: trino-deployment-requirements-install
category: computing-software
field: data-engineering
product: trino
tags: [requirements, java-25, ulimits, installation, server-tarball]
level: practitioner
status: docs-checked
description: "Trino server host requirements (64-bit Linux, ulimits, Java 25 Temurin), tarball choices and the install and data directory split."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/installation/deployment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino deployment requirements install

Linux: 64-bit, a newer release preferred (especially for containers), and adequate limits for the user running Trino. Open file descriptors scale roughly with the number of machines times a workload factor; `nofile` caps descriptors and `nproc` caps processes and thus JVM threads. Minimum recommended in `/etc/security/limits.conf`:

```text
trino soft nofile 131072
trino hard nofile 131072
trino soft nproc 128000
trino hard nproc 128000
```

Java: a 64-bit Java 25, minimum 25.0.1, latest patch recommended. Java 8, 11, 17, 21 and 24 do not work; Java 26 and newer are untested. Eclipse Temurin from Adoptium is what Trino is tested against and what the Docker image uses.

Install: download and unpack the server tarball, which contains one top-level directory (the installation directory). The default tarball holds all plugins, which must be configured before use. The `server-core` tarball has only essential plugins and suits building custom tarballs. The trino-packages project can build a fully configured tarball with example configuration.

Trino needs a data directory for logs and more. By default it equals the installation directory, but putting it outside the installation directory preserves it across upgrades; set it with `node.data-dir`. The Trino user needs full read access to the installation directory and read-write access to the data directory.

## Checked

2026-11-04. Read against the Trino docs page `installation/deployment.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
