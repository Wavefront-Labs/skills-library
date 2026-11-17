---
id: computing-software.systems-network-administration.linux.registries-conf-mirrors-and-short-name-policy
name: registries-conf-mirrors-and-short-name-policy
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, registries-conf, short-name-aliases, registry-mirror, short-name-mode, containers-registries, insecure-registry]
level: practitioner
status: docs-checked
description: "Configure /etc/containers/registries.conf for Podman, Skopeo and CRI-O: unqualified-search registries, short-name mode and aliases, mirrors, blocking and insecure registries."
sources:
  - https://github.com/containers/image/blob/main/docs/containers-registries.conf.5.md
  - https://www.redhat.com/en/blog/container-image-short-names
  - https://github.com/containers/image/blob/main/docs/containers-registries.conf.d.5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# registries.conf mirrors and short-name policy

Applies to everything built on containers/image: Podman, Buildah, Skopeo, CRI-O. Files: `/etc/containers/registries.conf`,
and the per-user `$HOME/.config/containers/registries.conf`, which container engines use if it exists, otherwise the
system file (the user file is not merged with it). Drop-in files in `registries.conf.d` are described in
containers-registries.conf.d(5).

## Short names
`podman pull nginx` is ambiguous: which registry? Controlled by:
```toml
unqualified-search-registries = ["registry.access.redhat.com", "docker.io"]
short-name-mode = "enforcing"     # enforcing | permissive | disabled
```
- `unqualified-search-registries` is the list of registries to try, in order, for an unqualified image.
- `enforcing`: with one search registry, use it; with several and a terminal (TTY), prompt the user; without a terminal,
  fail with an error.
- `permissive`: like enforcing, but without a terminal it falls back to trying all search registries instead of erroring.
  It is the default when `short-name-mode` is unset or empty.
- `disabled`: use all unqualified-search registries without prompting.
- Aliases resolve short names deterministically, in an `[aliases]` table of `"name" = "value"`:
```toml
[aliases]
"nginx" = "docker.io/library/nginx"
"ubi9"  = "registry.access.redhat.com/ubi9/ubi"
```
  After you pick a registry at a prompt, Podman records an alias in the user's `short-name-aliases.conf` under
  `$HOME/.config/containers/` (for root, under `/var/cache/containers/`), so you are not prompted again.
Best practice in scripts, Containerfiles and Quadlets: use fully qualified image names.

## Mirrors
```toml
[[registry]]
prefix = "docker.io"
location = "docker.io"
  [[registry.mirror]]
  location = "mirror.example.com/dockerhub"
  [[registry.mirror]]
  location = "registry-cache.local:5000"
  insecure = true
```
Mirrors are tried in the specified order; the first one that can be contacted and has the image is used. A
`pull-from-mirror` value of `digest-only` limits mirror use to digest pulls (`all` and `tag-only` are the other values),
which suits mirrors where tags may lag. To redirect a namespace, set `prefix` to the namespace and `location` to the
internal registry (see "Remapping and mirroring registries" in containers-registries.conf(5)).

## Block and insecure
```toml
[[registry]]
location = "untrusted.example.net"
blocked = true

[[registry]]
location = "lab-registry:5000"
insecure = true
```
`blocked = true` forbids pulling images with matching names. By default container runtimes require TLS; `insecure`
relaxes that, so prefer trusting the registry's CA (see containers-certs.d(5)).

## Verify
- [ ] Short-name pulls resolve to the intended registry without prompting; mirror use confirmed from the engine's
  debug output.
- [ ] A pull from a blocked registry fails.

## Checked
2026-10-28. Confirmed in containers-registries.conf(5), containers-registries.conf.d(5) and the Red Hat short-names
blog: file precedence, `unqualified-search-registries`, the three `short-name-mode` modes and the permissive default,
`[aliases]`, alias recording locations, mirror order, `pull-from-mirror`, `blocked`, `insecure`, `prefix`/`location`.
Corrected: alias file path (was `~/.cache/containers/...`). Removed as unconfirmed: the debug and `podman info` commands,
quoted error messages, the `certs.d` path.
Method: documentation only; no commands were run.
