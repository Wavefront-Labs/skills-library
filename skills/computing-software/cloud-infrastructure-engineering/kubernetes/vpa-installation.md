---
id: computing-software.cloud-infrastructure-engineering.kubernetes.vpa-installation
name: vpa-installation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, vpa, vpa-install, vertical-pod-autoscaler, metrics-server]
level: practitioner
status: docs-checked
description: "Install the Vertical Pod Autoscaler (recommender, updater, admission controller) with vpa-up.sh or Helm, its certificates and prerequisites, and verify it."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/installation.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/charts/vertical-pod-autoscaler/README.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/flags.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/examples.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing VPA

## Prerequisites
- metrics-server working (`kubectl top pods`).
- Optional: Prometheus for history (recommender `--storage=prometheus`; the default storage
  mode is `checkpoint`).
- No other VPA installation already present.

## Upstream script
```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
git checkout vertical-pod-autoscaler-1.8.1       # tag of a release; the docs name 1.8.1 as the current default
./hack/vpa-up.sh
```
Starts the VPA components in the `kube-system` namespace and generates and uploads a CA cert
secret used by the admission controller (needs openssl 1.1.1 or later for `-addext`).
`./hack/vpa-process-yamls.sh print` prints the resources without applying them. Teardown:
`./hack/vpa-down.sh`. If another VPA version is installed, tear it down first.

## Helm (chart in the autoscaler repo)
```bash
helm repo add autoscalers https://kubernetes.github.io/autoscaler
helm upgrade -i vertical-pod-autoscaler autoscalers/vertical-pod-autoscaler \
  --set updater.enabled=false   # start recommend-only
```
The chart README marks the chart as under development and not ready for production use.
Its values include `admissionController.enabled`, `recommender.enabled` and `updater.enabled`
(all true by default). Starting with the updater disabled gives recommendations without evictions.

## Components
| Component | Does |
|---|---|
| recommender | watches usage, writes `status.recommendation` |
| updater | evicts pods whose requests are far from recommendation (Recreate/Auto modes) |
| admission-controller | mutating webhook that sets requests on new pods |

## Verify
```bash
kubectl -n kube-system get pods
kubectl get mutatingwebhookconfiguration vpa-webhook-config
kubectl apply -f examples/hamster.yaml   # from the vertical-pod-autoscaler directory
kubectl describe vpa hamster-vpa
```
The webhook `failurePolicy` is `Ignore` unless the admission controller runs with
`--webhook-failure-policy-fail=true`, so webhook failures do not block pod creation but stop VPA
from applying requests; monitor admission controller logs.

## Checked

Checked 2026-10-24 against the kubernetes/autoscaler vertical-pod-autoscaler docs (master): installation.md (current default VPA 1.8.1, `hack/vpa-up.sh`, `hack/vpa-down.sh`, `vpa-process-yamls.sh print`, openssl `-addext` note, kube-system namespace), flags.md (`storage` default `checkpoint`, `webhook-failure-policy-fail` default false), the in-repo Helm chart README and values.yaml (repo URL, `updater.enabled`, `recommender.enabled`, `admissionController.enabled`), faq.md (`vpa-webhook-config`).

Method: documentation only; no commands were run.
