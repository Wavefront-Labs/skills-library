---
id: computing-software.cybersecurity-defensive.pomerium.session-recording-extension-setup
name: session-recording-extension-setup
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [session-recording, envoy-dynamic-extensions, enterprise-image, ssh-recording, extension-so]
level: advanced
status: docs-checked
description: "Enable Pomerium Enterprise SSH session recording: obtain the Envoy extension, set its path, connect storage and turn recording on per route."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/session-recording.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSH session recording is an Enterprise feature and needs native SSH access configured. Recording is not in binary distributions; it needs an extension loaded from disk at startup.

1. **Get the extension.** The enterprise image `docker.cloudsmith.io/pomerium/pomerium-enterprise/pomerium-enterprise` drops in for `pomerium/pomerium` and ships `/extensions/session_recording_extension.so`. The ingress controller equivalent is `.../ingress-controller-enterprise`. A standalone image `docker.cloudsmith.io/pomerium/enterprise/session-recording-extension` is tagged `vX.Y.Z` for official Pomerium releases; for unreleased or self-built Pomerium the tag must match the Envoy version (from the `envoy-version` startup log field, `pomerium --version`, or `go.mod`).
2. **Set the absolute path** `/extensions/session_recording_extension.so` via Console (Settings, Global, Extension File Paths), `envoy_dynamic_extensions` in config.yaml or Terraform, or `envoyDynamicExtensions` on the Pomerium CR.
3. **Storage**: set `blob_storage.bucket_uri` or an Enterprise datasource (see recording-blob-gcs-s3). The instance must connect to Enterprise at least once to get a cluster ID.
4. **Enable per route**: `session_recording` with `enabled: true` (Terraform `session_recording = { enabled = true }`).

Verify: no extension errors at startup, upload messages after a session, and the recording on the Recordings page seconds after the session ends.

Recordings capture the terminal without redaction, so they may hold secrets.

## Checked

2026-11-04. Read the SSH Session Recording page: Enterprise and native SSH prerequisites, image names, extension path, Console and config key locations, storage and cluster ID note, per-route flag, verification steps and the no-redaction warning confirmed. Corrected the standalone image tagging rule, which the page ties to the Pomerium version for official releases and to the Envoy version otherwise.

Method: documentation only; no commands were run.
