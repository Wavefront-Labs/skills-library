---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-runtime-hooks-configure
name: tetragon-runtime-hooks-configure
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [runtime-hooks-config]
level: advanced
status: docs-checked
description: "Configure Tetragon runtime hooks installation: the host install directory and which namespaces may start containers when the agent is unreachable."
sources:
  - "https://tetragon.io/docs/installation/runtime-hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure runtime hooks installation

## Installation directory (`rthooks.installDir`)

The `tetragon-rthooks` daemonset installs the `tetragon-oci-hook` binary on the host, in `/opt/tetragon` by default. If `/opt` is read-only, the pod fails with a `FailedMount` error such as `mkdir /opt/tetragon: read-only file system`. Choose another location:

```
--set rthooks.installDir=/run/tetragon
```

## Failure check

`tetragon-oci-hook` logs to `/opt/tetragon/tetragon-oci-hook.log`. When it cannot reach the agent it logs a WARN ("hook request to the agent failed", for example a context deadline exceeded for `unix:///var/run/tetragon/tetragon.sock`), followed by an INFO "failCheck determined that we should not fail this container". The hook checks container annotations and by default does not fail a container in the same namespace as Tetragon, so Tetragon's own pods can start.

To let containers in other namespaces start when the agent is unreachable, use one or both options.

Exact names, comma-separated:

```yaml
rthooks:
  enabled: true
  failAllowNamespaces: namespace1,namespace2
```

RE2 regex patterns (a container starts if its namespace matches any pattern). Matching is substring by default, so use `^` and `$` for full-string matching: `^kube-.*$` (prefix), `^.*-system$` (suffix), `^foo-.*-bar$`, and `.*` (matches every namespace, disabling the hook for all). Without anchors, `acme-` also matches `not-acme-foo`.

```yaml
rthooks:
  enabled: true
  failAllowNamespaces: kube-system
  failAllowNamespacesRegex:
    - "^acme-.*$"
    - "^dev-.*$"
```

Combined, a container is allowed if its namespace matches either an exact name or any regex.

If the pod namespace annotation is missing from the container annotations, the hook always fails the container (safe default). Both options are ignored when `extraHookArgs` sets `fail-cel-expr`, which always takes precedence.

## Checked

2026-11-08. Read the runtime hooks installation page in full (raw docs markdown). Checked installDir and the failure check options against it; no claims removed.

Method: documentation only; no commands were run.
