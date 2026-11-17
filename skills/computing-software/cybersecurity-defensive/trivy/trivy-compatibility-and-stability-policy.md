---
id: computing-software.cybersecurity-defensive.trivy.trivy-compatibility-and-stability-policy
name: trivy-compatibility-and-stability-policy
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [compatibility, stability, stable-interfaces, schema-version, json-output, breaking-changes]
level: advanced
status: docs-checked
description: "What Trivy promises to keep stable (CLI, config, exit codes, output formats), what it does not (scan results, Go APIs, client/server compatibility), and how SchemaVersion changes."
sources:
  - https://trivy.dev/latest/docs/guide/references/compatibility/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy is primarily a CLI application and strives to preserve compatibility for documented user-facing interfaces, except for features explicitly marked experimental or subject to change.

Stable interfaces: CLI commands, subcommands, flags and arguments; configuration file options and environment variables; exit codes and the conditions returning them; machine-readable output formats; data fields used by custom templates. Adding a new command, flag, option or output field is compatible as long as it does not change existing usage. When documentation and implementation disagree, neither is automatically authoritative.

JSON output includes `SchemaVersion`. Within one version, optional fields may be added or omitted, so consumers should ignore unknown fields and must not assume optional fields are always present. Removing or renaming a field, changing its type, or changing its meaning incompatibly generally requires a `SchemaVersion` update and a breaking-change note in the release notes.

Outside the policy: Go packages and APIs (Trivy is not designed or supported as a Go library); build tool versions and scripts; exact formatting of terminal output, logs and errors; scan results including their content and ordering; internal formats such as caches, vulnerability databases, internal RPC and Protocol Buffers; compatibility between different Trivy client and server versions; experimental or preview features, canary builds and prereleases; and behaviour changes caused by external specifications, services or data sources. These may change without a deprecation period.

A breaking change is one that forces users to modify an existing valid use of a stable interface. Deprecations are announced when practical, with no fixed period guaranteed, and urgent security issues can bypass the usual process.

## Checked

2026-11-03. Read and confirmed against the Compatibility and Stability page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
