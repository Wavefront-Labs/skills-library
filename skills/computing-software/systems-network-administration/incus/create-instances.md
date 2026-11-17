---
id: computing-software.systems-network-administration.incus.create-instances
name: create-instances
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, launch, init, container, virtual-machine, oci, instance-type, target]
level: practitioner
status: docs-checked
description: "Create Incus containers and VMs with incus launch/init: image syntax, --vm, --config, --device, --profile, --network, --storage, --target, --type and YAML via stdin."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create instances

`incus init` creates; `incus launch` creates and starts.

```
incus launch <image_server>:<image_name> <instance_name> [flags]
incus launch images:debian/12 debian-container
incus launch images:debian/12 debian-vm --vm
incus launch images:debian/12 debian-vm --vm --device root,size=30GiB
incus launch images:debian/12 c1 --config limits.cpu=1 --config limits.memory=192MiB
incus launch images:debian/12 c2 --vm --target server2
incus launch images:debian/12 c3 --type t2.micro
incus launch oci-docker:hello-world --ephemeral --console
incus launch images:debian/12 debian-config < config.yaml
```

- Names must be unique across the whole deployment, including clusters.
- Flags: `--config`, `--device` (override a profile device or set root disk), `--profile`, `--network`, `--storage`, `--target` (cluster member), `--vm`.
- `--type` accepts `<instance type>`, `<cloud>:<instance type>` or `c<CPU>-m<RAM in GiB>`.
- OCI (application) containers need an OCI registry added as a remote first.
- For YAML syntax, copy from `incus config show <name> --expanded`.

## Checked

2026-11-04: confirmed against the Incus create-instances how-to (init versus launch, image syntax, name uniqueness, common flags, OCI registry requirement, instance type forms, YAML via stdin). Nothing removed.

Method: documentation only; no commands were run.
