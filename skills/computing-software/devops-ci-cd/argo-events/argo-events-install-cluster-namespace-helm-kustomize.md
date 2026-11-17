---
id: computing-software.devops-ci-cd.argo-events.argo-events-install-cluster-namespace-helm-kustomize
name: argo-events-install-cluster-namespace-helm-kustomize
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, install, kubectl, helm, kustomize, namespace-install, openshift, validating-webhook]
level: intro
status: docs-checked
description: "Install Argo Events cluster-wide, namespace-scoped, with Kustomize or Helm, plus the GKE and OpenShift adjustments and the default EventBus."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events install cluster namespace helm kustomize

Requirements: Kubernetes 1.11 or later and kubectl newer than 1.11.0.

Cluster-wide: create the `argo-events` namespace, then apply `manifests/install.yaml` from the stable branch (service account, ClusterRoles and controllers for Sensor, EventBus and EventSource). `install-validating-webhook.yaml` installs the same with a validating admission controller. Namespace-scoped: apply `namespace-install.yaml` instead. In either case deploy an EventBus afterwards, for example the `native.yaml` example (`kubectl apply -n argo-events -f` its raw URL).

Notes:
- GKE: you may need `kubectl create clusterrolebinding ... --clusterrole=cluster-admin --user=<your email>` to create CRDs and ClusterRoles.
- OpenShift: grant the `anyuid` SCC to the service accounts (`argo-events-sa` and `argo-events-webhook-sa` for cluster install, `default` for namespace install), and for the validating webhook add `update` on `deployments/finalizers` and `clusterroles/finalizers` to the argo-events-webhook ClusterRole.

Kustomize: use the `cluster-install`, `cluster-install-with-extension` or `namespace-install` folder as a base. Helm: `helm repo add argo https://argoproj.github.io/argo-helm`, then `helm install argo-events argo/argo-events -n argo-events --create-namespace`; the chart is community-maintained, so controller image versions may lag and you should set the image in values.yaml to v1.0.0. Upgrading from before 0.16.0 needs the project migration notes.

The EventBus example the page applies is `examples/eventbus/native.yaml`; the NATS Streaming EventBus it creates is deprecated in favour of JetStream (EventBus pages).

## Checked

2026-11-04. Confirmed against the Installation page: requirements, cluster-wide and namespace steps and manifest names, the validating-webhook manifest, GKE and OpenShift notes (service accounts, finalizers rules), the EventBus step, the Kustomize folders, the Helm commands and community-maintenance warning with the `values.yaml` image advice, and the pre-0.16.0 migration pointer. Added the note that `native.yaml` is the deprecated NATS Streaming bus.
Method: documentation only; no commands were run.
