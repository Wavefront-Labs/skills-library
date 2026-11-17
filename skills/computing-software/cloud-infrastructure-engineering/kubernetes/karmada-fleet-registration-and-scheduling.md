---
id: computing-software.cloud-infrastructure-engineering.kubernetes.karmada-fleet-registration-and-scheduling
name: karmada-fleet-registration-and-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-cluster, karmada, open-cluster-management, liqo, cluster-registration, fleet-kubeconfig, propagationpolicy]
level: advanced
status: docs-checked
description: "Register clusters into a Karmada (or OCM) fleet in push or pull mode and schedule workloads across them with PropagationPolicy, replica division and failover."
sources: ["https://karmada.io/docs/userguide/clustermanager/cluster-registration/", "https://karmada.io/docs/userguide/scheduling/propagation-policy/", "https://karmada.io/docs/userguide/failover/application-failover/", "https://karmada.io/docs/installation/install-cli-tools/", "https://open-cluster-management.io/docs/getting-started/installation/register-a-cluster/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Karmada fleet: cluster registration and workload scheduling

Karmada runs a Kubernetes-API control plane (karmada-apiserver) where you apply ordinary
manifests plus policies; it propagates them to member clusters.

## Registration
```bash
# karmadactl (also installable as the kubectl plugin: kubectl krew install karmada)
# Push mode: the control plane connects to the member's kube-apiserver
karmadactl join prod-eu --kubeconfig=karmada-apiserver.config \
  --cluster-kubeconfig=prod-eu.kubeconfig --cluster-context=prod-eu
# Pull mode: karmada-agent in the member pulls from the control plane
karmadactl token create --print-register-command --kubeconfig karmada-apiserver.config   # bootstrap token, default TTL 24h
karmadactl register <karmada-apiserver>:32443 --token <t> --discovery-token-ca-cert-hash sha256:<h> --cluster-name prod-us
kubectl --kubeconfig karmada-apiserver.config get clusters
```
Pull mode needs the `kube-public/cluster-info` ConfigMap in the control plane to name a `server` signed by
the root CA and reachable from members. Use a dedicated least-privilege credential for push-mode members and protect the
Karmada control plane accordingly. Label clusters (for example `env`, `region`) for targeting.
OCM equivalent: `clusteradm init` on the hub, `clusteradm join` on the cluster to be managed (it installs a
klusterlet), then accept the join request on the hub.

## Propagation and scheduling
```yaml
apiVersion: policy.karmada.io/v1alpha1
kind: PropagationPolicy
metadata: {name: web, namespace: shop}
spec:
  resourceSelectors:
  - {apiVersion: apps/v1, kind: Deployment, name: web}
  - {apiVersion: v1, kind: Service, name: web}
  placement:
    clusterAffinity:
      labelSelector: {matchLabels: {env: prod}}
    replicaScheduling:
      replicaSchedulingType: Divided
      replicaDivisionPreference: Weighted
      weightPreference:
        dynamicWeight: AvailableReplicas       # split by spare capacity
    spreadConstraints:
    - {spreadByField: region, minGroups: 2}
  failover:
    application:
      decisionConditions: {tolerationSeconds: 120}
      purgeMode: Graciously
```
`OverridePolicy` changes fields per cluster. Check `kubectl get resourcebinding -n shop` and `work` objects for
what landed where.

## Gotchas
- `clusterAffinity` only defines the candidate set; combine with `spreadConstraints` to control how many
  clusters or groups are selected.
- `purgeMode: Graciously` waits for the application to be healthy on the new cluster, or a timeout, before
  evicting it from the old one; `decisionConditions.tolerationSeconds` sets how long to wait before failing over.

## Verify
- [ ] All member clusters are Ready; a test Deployment's replicas split per the policy.

## Checked

2026-10-26, against Karmada website docs (karmada-io/website, last push 2026-09-24: cluster-registration, propagation-policy, application-failover, install-cli-tools) and OCM docs for the clusteradm commands. Confirmed: `karmadactl join` and `register`, `--cluster-kubeconfig` / `--cluster-context`, `karmadactl token create --print-register-command` (default TTL 24h), cluster-info ConfigMap requirement, PropagationPolicy `replicaScheduling` (`Divided`, `Weighted`, `dynamicWeight: AvailableReplicas`), `spreadConstraints`, `failover.application` (`decisionConditions.tolerationSeconds`, `purgeMode: Graciously`), krew install, `clusteradm init/join` and accept step. Removed unconfirmed kubectl-karmada init and cordon commands, Secret-storage and Liqo claims, and stateful-failover remarks.

Method: documentation only; no commands were run.
