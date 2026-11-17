---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-artifact-unit
name: quadlet-artifact-unit
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, artifact-unit, oci-artifact, artifact-pull, experimental, creds, authfile]
level: advanced
status: docs-checked
description: "Pull OCI artifacts with an experimental Quadlet .artifact: mandatory Artifact key, mapped podman artifact pull options and the unit's experimental warning."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fetch artifacts that containers will mount or read.

The page flags this unit as experimental: inputs, options and outputs are subject to change. An `.artifact` file has an `[Artifact]` section and generates a one-time service ensuring the artifact exists on the host, pulling it if needed. This is useful for artifacts containers need to mount or access. The `Artifact` key is mandatory.

Keys from the table, with their `podman artifact pull` equivalents: `Artifact=quay.io/foobar/artifact:special` (the artifact to pull), `AuthFile=` (`--authfile`), `CertDir=` (`--cert-dir`), `Creds=` (`--creds=username:password`), `DecryptionKey=` (`--decryption-key`), `Quiet=true` (`--quiet`), `Retry=` and `RetryDelay=`, `TLSVerify=false`, `ServiceName=my-artifact` (sets the service name to `my-artifact.service`), `ContainersConfModule=`, `GlobalArgs=` and `PodmanArgs=`.

Treat it like other generated one-time units: the file is processed by the generator, so use the dry-run debugging command when the service does not appear, and expect option changes in newer Podman versions.


Retry values shown in the table for pulls are `Retry=5` and `RetryDelay=10s`; both are available here when the registry is unreliable. `ServiceName=my-artifact` is the example that yields `my-artifact.service`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
