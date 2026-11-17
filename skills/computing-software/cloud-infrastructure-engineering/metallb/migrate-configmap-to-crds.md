---
id: computing-software.cloud-infrastructure-engineering.metallb.migrate-configmap-to-crds
name: migrate-configmap-to-crds
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, configmaptocrs, configmap-migration, crds, v0-13, quay-io, kubectl-run]
level: practitioner
status: docs-checked
description: "Convert a pre-v0.13 MetalLB ConfigMap to CRDs with the configmaptocrs container, offline against config.yaml or in-cluster to stdout, plus its flags."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/migration_to_crds.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating a ConfigMap to CRDs

Up to v0.12 MetalLB was configured by ConfigMap. From v0.13.0 only CRs configure it. The tool is the image `quay.io/metallb/configmaptocrs`.

Offline (assumes namespace `metallb-system`, ConfigMap named `config`):
```bash
kubectl get configmap -n metallb-system -o yaml config > config.yaml
docker run -d -v $(pwd):/var/input quay.io/metallb/configmaptocrs
```
Output: `resources.yaml` in the mapped folder, containing `BGPPeer` (v1beta2), `IPAddressPool` and `BGPAdvertisement` objects. For the docs' example, a pool with `aggregation-length: 32`, `localpref: 100` and communities becomes a `BGPAdvertisement` with `aggregationLength`, `localPref`, `communities` and `ipAddressPools`.

Directly against a cluster (prints CRs to stdout):
```bash
kubectl run configmaptocrs -n metallb-system --restart=Never -it --rm --image overriden --overrides '{...}'
```
The override sets the container image `quay.io/metallb/configmaptocrs`, command `/configmaptocrs -source config -only-data -stdout`, and mounts ConfigMap `config` at `/var/input` (full JSON in the source page).

Flags: `-source string` (input file, default `./config.yaml`), `-only-data bool` (input is just the ConfigMap data), `-stdout bool` (print CRDs).

Generated names are like `peer1` and `bgpadvertisement1`. Pool definitions: `computing-software.cloud-infrastructure-engineering.metallb.ipaddresspool-definition`.

## Checked

2026-11-04. Compared with the MetalLB "Migration to CRDs" page (container image, docker run and kubectl run commands, resources.yaml output, generated names, the three flags and their descriptions) and the MetalLB home page (v0.13.0 CRs-only statement). Removed the unsupported apply/verify steps.

Method: documentation only; no commands were run.
