---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-disable-packaged-components
name: k3s-disable-packaged-components
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, disable-flag, skip-file, traefik]
level: practitioner
status: docs-checked
description: "Disable Traefik, CoreDNS and other packaged components with --disable or .skip files, and know how each differs."
sources:
  - https://docs.k3s.io/installation/packaged-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two ways to stop manifests being deployed.

1. The --disable flag. Works for packaged component AddOns and any other manifests in the directory. Disabled AddOns are actively uninstalled from the cluster and their source files deleted from the manifests directory. Example: `--disable=traefik` installs a new cluster without Traefik or uninstalls it from an existing one. Separate several names with commas or repeat the flag.

2. .skip files. For any file under /var/lib/rancher/k3s/server/manifests, create a matching `.skip` file (only its existence matters, not its contents). Example: an empty traefik.yaml.skip created before the first start makes K3s skip traefik.yaml, leaving local-path-provisioner, metrics-server and coredns running.

Difference: creating a .skip file after an AddOn already exists does not remove or change it or its resources; the file is just treated as absent. If Traefik had already been deployed, it stays as it is and is not affected by future updates when K3s is upgraded.

## Checked

2026-11-08. Read the full K3s Managing Packaged Components page (docs/installation/packaged-components.md in the k3s-io/docs repo). Confirmed: --disable behaviour (actively uninstalls and deletes source files), comma or repeated flags, .skip file behaviour and example, and the already-deployed Traefik caveat. Removed the FAQ ingress sentence and the HA same-flag line (not on the page).

Method: documentation only; no commands were run.
