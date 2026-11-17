---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-operator-prometheus-cr
name: prometheus-operator-prometheus-cr
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-operator, prometheus-cr, prometheus-custom-resource, storage-spec, retention, external-labels, servicemonitor-selector]
level: practitioner
status: docs-checked
description: "Configure the Prometheus operator custom resource: persistent storage, retention, external labels, monitor and rule selectors, volume permissions and PVC resizing."
sources:
  - https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.Prometheus
  - https://prometheus-operator.dev/docs/platform/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The Prometheus custom resource

```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata: {name: k8s, namespace: monitoring}
spec:
  version: <prometheus-version>
  replicas: 2
  retention: 15d
  retentionSize: 80GB
  externalLabels: {cluster: prod-eu-1}
  scrapeInterval: 30s
  evaluationInterval: 30s
  resources:
    requests: {cpu: "1", memory: 8Gi}
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: <class>
        resources: {requests: {storage: 100Gi}}
  serviceAccountName: <service-account>
  serviceMonitorSelector: {}
  serviceMonitorNamespaceSelector: {}
  podMonitorSelector: {}
  probeSelector: {}
  ruleSelector: {matchLabels: {role: alert-rules}}
```
Field behaviour from the API reference:
- `version`: the operator uses it to generate the StatefulSet and configuration; if unset it assumes the latest upstream Prometheus available when that operator version was released.
- `replicas`: replicas of each shard; `spec.replicas` times `spec.shards` is the total number of Pods. Default 1.
- `retention`: default `24h` if `retention`, `retentionSize` and `retentionPercentage` are all empty. `retentionSize` caps bytes used by the data. `retentionPercentage` (0-100, 0 disables) needs Prometheus v3.11.0 or newer and is ignored by older versions.
- `scrapeInterval` and `evaluationInterval` both default to 30s.
- `externalLabels` are added to series and alerts when talking to external systems (federation, remote storage, Alertmanager). The operator also adds a replica label (`replicaExternalLabelName`, default `prometheus_replica`) and a `prometheus` instance label (`prometheusExternalLabelName`, default `prometheus`); these take precedence over `externalLabels`, and setting either name to the empty string omits it.
- `walCompression` (Snappy) is enabled by default for Prometheus 2.20.0 and later.
- `enableAdminAPI` enables mutating endpoints (delete data, shut down); the reference warns to put authentication in front of it.

## Selectors
- For `serviceMonitorSelector`, `podMonitorSelector`, `probeSelector` and `ruleSelector`: an empty selector (`{}`) matches all objects, a null (unset) selector matches none.
- The matching namespace selectors (`serviceMonitorNamespaceSelector`, `podMonitorNamespaceSelector`, `ruleNamespaceSelector`): empty matches all namespaces; null (the default) matches the current namespace only.
- If `serviceMonitorSelector`, `podMonitorSelector`, `probeSelector` and `scrapeConfigSelector` are all null, the Prometheus configuration is unmanaged: you must supply the gzipped config under the `prometheus.yaml.gz` key of the config Secret. This behaviour is deprecated; use `spec.additionalScrapeConfigs` instead.

## Storage
- With no `storage` the operator uses `emptyDir`, which is not persisted when Pods are redeployed. A PVC is created for each Pod in the StatefulSet from `volumeClaimTemplate`.
- For volumes that cannot be provisioned dynamically, use a `selector.matchLabels` in the claim template plus a manually created PersistentVolume (`ReadWriteOnce` is required). A default StorageClass can override manual provisioning.
- Volume permissions: the Prometheus container runs as non-root (`nobody`, UID 65534 in the default image) and the operator sets no Pod security context unless you do. A root-owned unwritable volume (common with NFS or CephFS) crash-loops the Pod; set `securityContext` with `fsGroup: 65534`, `runAsNonRoot: true`, `runAsUser: 65534`. `fsGroup` may not take effect on some volume types (for example NFS); then fix permissions on the storage side.
- Resizing: Kubernetes does not support volume expansion through StatefulSets, so editing `spec.storage` makes the operator delete and recreate the StatefulSet without expanding PVCs. Documented manual fix:
  1. Check the StorageClass has `allowVolumeExpansion: true`.
  2. Patch the CR with `spec.paused: true` and the new storage request.
  3. Patch every PVC (`-l operator.prometheus.io/name=<name>`) with the new request.
  4. `kubectl delete statefulset -l operator.prometheus.io/name=<name> --cascade=orphan`.
  5. Set `spec.paused` back to `false`; the operator recreates the StatefulSet with no service disruption.

## Verify
- [ ] PVCs are bound and the Pods run as the intended user.
- [ ] The Prometheus configuration page lists a job for every expected monitor; if not, compare the selector with the monitor's labels.

## Checked
Checked 2026-11-08 against the operator API reference for the Prometheus resource and the storage platform page. Removed because the pages do not state them: kube-prometheus-stack Helm values, `podAntiAffinity`, a specific Prometheus version, "~80% of the PVC" sizing, "whichever retention limit hits first wins", Thanos/Mimir dedup label advice, rolling upgrade order, and kubectl status columns.

Method: docs-only read of cited pages, 2026-11-08
