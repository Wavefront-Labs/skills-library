---
id: computing-software.cloud-infrastructure-engineering.kubespray.offline-environment-required-artifacts
name: offline-environment-required-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [offline, air-gapped, mirror, registry, artifacts, generate-list]
level: practitioner
status: docs-checked
description: "List what an air-gapped Kubespray deployment needs: static files, OS packages, container images, optional Python packages and Helm charts, and the services that serve them."
sources:
  - https://kubespray.io/docs/operations/offline-environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When servers have no direct internet access, fetch these artifacts in advance from an environment that does:

- Some static files (zips and binaries)
- OS packages (rpm/deb files)
- Container images used by Kubespray (the exhaustive list depends on your setup)
- Optional: Python packages from `requirements.txt` (only if your OS does not provide all of them)
- Optional: Helm chart files (only if `helm_enabled: true`)

Then provide these services inside the offline network:

- an HTTP reverse proxy, cache or mirror for static files
- an internal Yum/Deb repository for OS packages
- an internal container image registry populated with all images
- optional: an internal PyPi server
- optional: an internal Helm registry

Artifact lists come from the `generate_list.sh` script, and the repository has more helper tools under `contrib/offline`.

Two tips from the page: use the original domains as top directories in the files repo (`github.com/`, `dl.k8s.io/`, `storage.googleapis.com/`, `get.helm.sh/`); and for Cilium mirror `https://helm.cilium.io/index.yaml` plus the chart `cilium-1.18.2.tgz` in the files repo.

The chart version in that tip belongs to the docs revision I checked, so confirm it against your Kubespray tag.

## Checked

Artifact and service lists and both tips were confirmed on the Offline environment page.

Method: docs-checked 2026-11-09 against the Kubespray docs/operations/offline-environment.md page (full file read).
