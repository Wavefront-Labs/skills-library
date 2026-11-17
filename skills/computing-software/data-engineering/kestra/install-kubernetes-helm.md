---
id: computing-software.data-engineering.kestra.install-kubernetes-helm
name: install-kubernetes-helm
category: computing-software
field: data-engineering
product: kestra
tags: [kubernetes, helm, kestra-starter, ingress, scaling, dind]
level: practitioner
status: docs-checked
description: "Deploy Kestra on Kubernetes with the kestra or kestra-starter Helm chart, access the UI, configure ingress, scale components, and handle Docker-in-Docker."
sources:
  - https://kestra.io/docs/installation/kubernetes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Needs kubectl and Helm. Two charts:

- `kestra`: production, no bundled database or storage, runs standalone mode (all core components in one pod).
- `kestra-starter`: bundles PostgreSQL and Versity (S3-compatible). Evaluation only.

```bash
helm repo add kestra https://helm.kestra.io/
helm repo update
helm install my-kestra kestra/kestra-starter
```

Reach the UI with `kubectl port-forward $POD_NAME 8080:8080`, selecting the pod by label `app.kubernetes.io/component=standalone`.

Ingress: put `ingress:` at the top of `values.yaml` for `kestra`, or nest it under `kestra:` for `kestra-starter`. Apply with `helm upgrade my-kestra kestra/kestra-starter -f values.yaml`.

Scaling: set `standalone.enabled: false` and enable `webserver`, `executor`, `indexer`, `scheduler`, `worker`, `controller` under `deployments`. Workers reach the controller over gRPC on port 50051, so network policies must allow it. Set the endpoint under `configurations.application.kestra.worker.controllers`.

Config under `configurations.application` mirrors `application.yml`. Inject secrets with `common.extraEnvFrom` and a `secretRef`.

Workers use rootless Docker-in-Docker by default. To avoid it, set `dind.enabled: false` and use the Kubernetes task runner.

## Checked

2026-11-04. Confirmed against the Kestra Kubernetes page: the kestra and kestra-starter charts and what they bundle, helm repo add and install commands, standalone pod label selector and port-forward on 8080, ingress placement for each chart and the helm upgrade command, scaling values with standalone disabled and gRPC port 50051, configurations.application, common.extraEnvFrom with secretRef, rootless Docker-in-Docker default and dind.enabled false with the Kubernetes task runner. Nothing removed.

Method: documentation only; no commands were run.
