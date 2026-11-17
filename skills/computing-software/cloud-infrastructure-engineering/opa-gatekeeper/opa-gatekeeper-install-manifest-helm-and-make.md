---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-install-manifest-helm-and-make
name: opa-gatekeeper-install-manifest-helm-and-make
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, install, helm, manifest, rbac, kubectl, prerequisites]
level: intro
status: docs-checked
description: "Install OPA Gatekeeper from the release manifest, Helm chart or make, with the cluster-admin prerequisite and the minimum Kubernetes version note."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/install.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper install manifest helm and make

Gatekeeper needs cluster admin rights and a Kubernetes version within the supported-versions policy (it needs resources introduced in v1.16). Grant yourself admin first if needed:

```sh
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole cluster-admin --user <YOUR USER NAME>
```

Three install routes:
- Prebuilt release manifest: `kubectl apply -f` the `deploy/gatekeeper.yaml` file in the gatekeeper repository (raw GitHub URL on the master branch).
- Helm v3: `helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts`, then `helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace`. If you used the older repo location with Helm 3.3.2+, add `--force-update` to `helm repo add`. Warnings about the `crd-install` hook are expected (kept for Helm v2 compatibility) and harmless. Customise values in `charts/gatekeeper/values.yaml`.
- From HEAD with make: needs Docker 20.10+, a kubectl context for the target cluster and a registry the cluster can read. Run `make docker-buildx REPOSITORY=<registry> OUTPUT_TYPE=type=registry`, then `make deploy REPOSITORY=<registry>`. Omit `OUTPUT_TYPE` to build a local image.

Development images are tagged `openpolicyagent/gatekeeper:dev` or `:<SHA>` on Docker Hub.

## Checked

2026-11-04. Confirmed against install.md (prerequisites, release manifest, make, Helm, development images). Removed or corrected: nothing.

Method: documentation only; no commands were run.
