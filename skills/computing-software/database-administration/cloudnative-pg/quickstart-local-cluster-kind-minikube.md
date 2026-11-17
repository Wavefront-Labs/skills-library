---
id: computing-software.database-administration.cloudnative-pg.quickstart-local-cluster-kind-minikube
name: quickstart-local-cluster-kind-minikube
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [quickstart, kind, minikube, kubectl, cluster-example, labels]
level: intro
status: docs-checked
description: "Stand up a throwaway CloudNativePG cluster on Kind or Minikube: apply cluster-example.yaml, list pods by cnpg.io/cluster label, pin the image."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Quickstart is for demonstration and practice only, never production. Create a local Kubernetes cluster first:

```sh
minikube start
kubectl get nodes
```

or, without a VM hypervisor, `kind create cluster --name pg`. Then install the operator (see the installation skill) and apply the sample `Cluster`:

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: cluster-example
spec:
  instances: 3

  postgresql:
    synchronous:
      method: any
      number: 1

  storage:
    size: 1Gi
```

```sh
kubectl apply -f cluster-example.yaml
kubectl get pods
```

The operator labels every object of a cluster with `cnpg.io/cluster`, so `kubectl get pods -l cnpg.io/cluster=<CLUSTER>` isolates one cluster. The older `postgresql` label is being deprecated and will be dropped; use `cnpg.io/cluster`.

Without `imageName` you get the latest minor of the latest major PostgreSQL available when the operator was released. To choose a version set for example `imageName: ghcr.io/cloudnative-pg/postgresql:13.6`. For production always point at a specific tag, never `latest` or a bare major such as `13`; for strictly repeatable deployments append the digest as `<image>:<tag>@sha256:<digestValue>`.

## Checked

2026-11-08. Read in full: docs/src/quickstart.md. Commands, sample Cluster manifest and the cnpg.io/cluster label note confirmed on the Quickstart page, which states the steps are not for production.

Method: documentation only; no commands were run.
