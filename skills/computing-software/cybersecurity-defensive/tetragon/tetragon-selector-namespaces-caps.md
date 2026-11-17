---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-selector-namespaces-caps
name: tetragon-selector-namespaces-caps
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [selector-ns-caps, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Filter Tetragon hooks on Linux namespaces, capabilities and changes to either since process exec, e.g. to catch container escapes."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon namespace and capability filters

## matchNamespaces

```yaml
- matchNamespaces:
  - namespace: Pid
    operator: In
    values:
    - "4026531836"
    - "4026531835"
```

- `namespace`: `Uts`, `Ipc`, `Mnt`, `Pid`, `PidForChildren`, `Net`, `Cgroup`, `User`; `Time` and `TimeForChildren` on Linux >= 5.6.
- `operator`: `In` or `NotIn`.
- `values`: numeric inodes (e.g. from `lsns`) or `"host_ns"`.
- Values within a namespace are ORed; different `namespace` entries are ANDed.
- Limits: up to 4 values per namespace; up to 4 namespace entries on kernels < 5.3, up to 10 on >= 5.3.

Separate selectors (each starting with `-`) are ORed. Example: `/bin/cat` opening `/etc/shadow` (hook `fd_install`, args `int` and `file`) in the host `Mnt` namespace OR the host `Net` namespace needs two selectors; to require both host `Mnt` AND `Net`, put both namespace entries in one selector:

```yaml
matchNamespaces:
- namespace: Mnt
  operator: In
  values:
  - "host_ns"
- namespace: Net
  operator: In
  values:
  - "host_ns"
```

## matchCapabilities

```yaml
- matchCapabilities:
  - type: Effective
    operator: In
    values:
    - "CAP_CHOWN"
    - "CAP_NET_RAW"
```

`type`: `Effective`, `Inheritable` or `Permitted` (only one type per `matchCapabilities`). `operator`: `In` or `NotIn`. Values are capability names (see `/usr/include/linux/capability.h`); no limit on count.

## matchNamespaceChanges

Matches when a call changes Linux namespaces since the process's `process_exec` (when namespaces were recorded). Useful for new namespaces and container escapes; an unprivileged process creating a user namespace gets full privileges inside it. Test with `unshare` or `nsenter`.

```yaml
matchNamespaceChanges:
- operator: In
  values:
  - "Mnt"
```

## matchCapabilityChanges

Same idea for capabilities, compared with the set recorded at `process_exec`:

```yaml
matchCapabilityChanges:
- type: Effective
  operator: In
  isNamespaceCapability: false
  values:
  - "CAP_SETUID"
```

## Checked

2026-11-08. Read the selectors page in full (raw docs markdown from cilium/tetragon). Checked namespace, capability and change filters against it; no claims removed.

Method: documentation only; no commands were run.
