---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.kube-prometheus-stack-values-and-crd-upgrades
name: kube-prometheus-stack-values-and-crd-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [kube-prometheus-stack-values, kube-prometheus-crd-upgrade, kube-prometheus-stack, helm, prometheus-operator, upgrade]
level: practitioner
status: docs-checked
description: "Configure kube-prometheus-stack Helm values that matter (selectors, storage, retention, default rules, control plane) and upgrade it safely including manual CRD updates."
sources: ["https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack", "https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/UPGRADE.md", "https://prometheus-operator.dev/docs/getting-started/installation/", "https://prometheus-operator.dev/docs/platform/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kube-prometheus-stack values and CRD upgrades

## Values worth setting
```yaml
prometheus:
  prometheusSpec:
    retention: 15d            # chart default 10d
    retentionSize: 45GB       # chart default ""
    replicas: 2
    resources: {requests: {cpu: "1", memory: 8Gi}, limits: {memory: 12Gi}}
    storageSpec:
      volumeClaimTemplate:
        spec: {storageClassName: gp3, resources: {requests: {storage: 50Gi}}}
    serviceMonitorSelectorNilUsesHelmValues: false   # pick up all ServiceMonitors
    podMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false
    externalLabels: {cluster: prod-eu1}
alertmanager:
  alertmanagerSpec: {replicas: 3}   # alertmanagerConfigSelector selects AlertmanagerConfig CRs
defaultRules:
  disabled: {NodeRAIDDegraded: true}   # map of rule name to true
kubeControllerManager: {enabled: false}   # disable components Prometheus cannot reach
kubeScheduler: {enabled: false}
kubeEtcd: {enabled: false}
grafana:
  admin:
    existingSecret: my-grafana-admin   # keys default to admin-user and admin-password
```
- The README says Prometheus by default discovers monitors labelled with the same release tag as the release, and
  that setting the `*SelectorNilUsesHelmValues` values to `false` removes the label filter.
- `helm show values oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack` lists every option.
- Control-plane ServiceMonitors (kubelet, kube-apiserver, controller-manager, scheduler, etcd, kube-proxy, coredns,
  kube-dns) authenticate with a bearer token Secret (`authorization`) and the `kube-root-ca.crt` ConfigMap. The chart
  renders the token Secret when `prometheus.serviceAccount.createTokenSecret` is true (default); the UPGRADE notes say
  that token is long-lived and does not expire. Supply your own Secret and clear the defaults if you scrape with a
  Prometheus this chart does not deploy.

## Upgrading
Per the README, with Helm v3 the chart's CRDs are not updated by default, a CRD update causes a major chart version
bump, and `appVersion` is the prometheus-operator version with matching CRDs. Two routes:
1. Set `crds.upgradeJob.enabled` (values.yaml: a job that applies the CRDs before the operator using Helm hooks;
   "in preview, off by default"; UPGRADE.md says it exists since chart 68.4.0).
2. Apply the CRDs yourself before `helm upgrade`. UPGRADE.md gives one command per CRD, for example (the version in
   the URL is the operator version for the chart major you are moving to):
```bash
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v<OPERATOR_VERSION>/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
```
   Repeat for alertmanagerconfigs, alertmanagers, podmonitors, probes, prometheusagents, prometheusrules,
   scrapeconfigs, servicemonitors and thanosrulers (the ten CRDs the README lists for removal).
Then `helm upgrade [RELEASE_NAME] [CHART]`. A major chart version change is an incompatible change needing manual
action; read UPGRADE.md for every major version crossed.

## Gotchas
- Client-side apply of the large CRDs fails with `metadata.annotations: Too long` (limit 262144 bytes). Use
  `kubectl apply --server-side` (the operator troubleshooting page adds `--force-conflicts`; server-side apply needs
  Kubernetes 1.22+). With Argo CD sync with `ServerSideApply=true`.
- Uninstalling the release does not remove the CRDs; the README lists `kubectl delete crd` for each.
- UPGRADE.md has examples of upgrades needing manual steps, such as deleting the kube-state-metrics Deployment
  with `--cascade=orphan` when going from 21.x to 22.x. Check the section for each major you cross.

## Verify
- [ ] The CRDs carry the operator version of the target chart (inspect `kubectl get crd prometheuses.monitoring.coreos.com -o yaml`).
- [ ] All targets up and rules loaded after upgrade.

## Checked
2026-11-08. Confirmed in the kube-prometheus-stack README (CRD handling, major-bump rule, ten CRD names, Argo CD
note, release-tag selector), `values.yaml` (every key above and its default, `crds.upgradeJob` preview note,
`defaultRules.disabled`, `grafana.admin.existingSecret`), UPGRADE.md (per-CRD `--server-side` commands, 68.4.0, token
Secret note, 21.x to 22.x `--cascade=orphan`) and the Prometheus Operator troubleshooting page (`--force-conflicts`,
Kubernetes 1.22). Removed: the `charts/crds/crds/` directory path, `helm diff` advice, the StatefulSet storageSpec
orphan-delete claim, the Grafana database backup claim, `adminPassword` and the `KubeCPUOvercommit` example,
because the pages do not state them.
Method: documentation only; no commands were run.
