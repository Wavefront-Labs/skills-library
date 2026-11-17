---
id: computing-software.systems-network-administration.incus.install-from-source
name: install-from-source
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, source-build, make, go, liblxc, cowsql, incusd]
level: advanced
status: docs-checked
description: "Build Incus from source: dependencies, make deps environment variables, make, PATH and LD_LIBRARY_PATH, and starting incusd with a group."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/installing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build Incus from source

1. Install dependencies: liblxc 5.0.0 or later and a recent Go (Debian's Go may be too old). The docs list packages for Alpine, Debian/Ubuntu and openSUSE.
2. Get the source: `git clone https://github.com/lxc/incus`, or unpack a release tarball (it bundles libraft and libcowsql).
3. Run `make deps`, then export the variables it prints: `CGO_CFLAGS`, `CGO_LDFLAGS`, `LD_LIBRARY_PATH`, `CGO_LDFLAGS_ALLOW`.
4. Run `make`. Allow at least 2 GiB of RAM.
5. Add `$(go env GOPATH)/bin` to `PATH` and point `LD_LIBRARY_PATH` at the deps directories.
6. Start the daemon, passing the environment through sudo: `sudo -E PATH=$PATH LD_LIBRARY_PATH=$LD_LIBRARY_PATH $(go env GOPATH)/bin/incusd --group sudo`.
7. On ARM64 install AAVMF instead of OVMF for UEFI VMs.

Also configure subuid/subgid for root (see incus-admin-group-and-subuid).

## Checked

2026-11-09. Confirmed against the Incus How to install page (source sections): liblxc 5.0.0, Go caveat, dependency packages for Alpine/Debian/Ubuntu/openSUSE, release tarball bundling libraft and libcowsql, make deps variables, make, 2GiB RAM, PATH and LD_LIBRARY_PATH, incusd --group sudo command, AAVMF note. Nothing removed.
Method: documentation only; no commands were run.
