---
id: computing-software.systems-network-administration.virtualisation.proxmox-oci-image-containers
name: proxmox-oci-image-containers
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [oci-container-pve, oci-images, lxc, proxmox, containers]
level: advanced
status: docs-checked
description: "Create Proxmox VE containers from OCI images (technology preview in recent releases): pulling images, application vs system containers, configuration and limits."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_pct
  - https://pve.proxmox.com/wiki/Roadmap
  - https://pve.proxmox.com/pve-docs/pct.conf.5.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OCI image based containers on Proxmox VE

**Goal:** run software published as Docker/OCI images directly as Proxmox VE containers, where supported.

## Status
Proxmox VE 9.1 (November 2025) added OCI images as container templates: full system containers can be created from suitable OCI images, and initial support for application containers is a technology preview. The web UI has a **Pull from OCI registry** button in a storage's CT Templates view, and you can also upload an OCI image manually. On older releases, run Docker or Podman in a VM; for maximum isolation and live migration the admin guide recommends nesting containers inside a VM.

## Workflow (where supported)
1. Storage with `vztmpl` content -> **CT Templates** -> use **Pull from OCI registry** with an image reference (`<registry>/<repository>:<tag>`), or upload an OCI image archive.
2. Create CT from that template as usual (ID, storage, network, resources).
3. Suitable full-distribution images become system containers; single-application images become **application containers**.
4. The `entrypoint` (default `/sbin/init`) and `env` options of the container configuration can be edited.

## Limits to plan for
- A container created from an OCI image still uses the existing LXC framework. Declarative multi-guest support based on the Compose Specification is a roadmap item, not something to rely on yet.
- The `host-managed` NIC option makes the host responsible for the interface's IP configuration, so the container should not run its own DHCP client or network manager on it; `cmode=shell` opens a shell inside the container without login.
- The `keepattrs` mount point option controls whether a mounted filesystem inherits ownership and permissions from the existing mount point directory, which some OCI images expect.
- Image provenance is your responsibility.

## When to use Docker in a VM instead
Multi-container stacks, frequent image updates, or anything needing the Docker API: run them in a VM (best isolation) or an unprivileged LXC with `nesting=1,keyctl=1` (keyctl is required to use Docker inside a container).

## Verify
`pct config <id>` shows the OCI-derived entrypoint/env; the service answers on its port and survives a CT restart.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.adoc OCI section, pct.conf.5-opts.adoc entrypoint, env, host-managed and keepattrs options) and the Proxmox VE Roadmap wiki page (9.1 release notes: OCI images as templates, application containers as technology preview, entrypoint and env editing). Removed the unconfirmed claims about compose, in-place updates, missing SSH servers and the unsupported status of Docker-in-LXC.

Method: documentation only; no commands were run.
