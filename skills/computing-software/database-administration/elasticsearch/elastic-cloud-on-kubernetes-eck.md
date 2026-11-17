---
id: computing-software.database-administration.elasticsearch.elastic-cloud-on-kubernetes-eck
name: elastic-cloud-on-kubernetes-eck
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, eck, elasticsearch-kubernetes, operator, elasticsearch-setup, kubernetes]
level: practitioner
status: docs-checked
description: "Deploy and operate Elasticsearch on Kubernetes with the ECK operator: install, Elasticsearch CRD with nodeSets, storage, upgrades, scaling and common pitfalls."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/cloud-on-k8s/volume-claim-templates.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/cloud-on-k8s/virtual-memory.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/cloud-on-k8s/accessing-services.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Cloud on Kubernetes (ECK)

**Goal:** run Elasticsearch on Kubernetes with an operator that handles certificates, rolling upgrades, scaling and node removal safely.

## Install operator
```bash
# <eck-version>: the current ECK release (see the ECK install docs / GitHub releases)
kubectl create -f https://download.elastic.co/downloads/eck/<eck-version>/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/<eck-version>/operator.yaml
kubectl -n elastic-system logs statefulset/elastic-operator
```

## Cluster definition
```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata: { name: prod, namespace: search }
spec:
  version: <stack-version>
  nodeSets:
  - name: masters
    count: 3
    config: { node.roles: ["master"] }
    volumeClaimTemplates:
    - metadata: { name: elasticsearch-data }
      spec: { accessModes: [ReadWriteOnce], storageClassName: fast-ssd, resources: { requests: { storage: 20Gi } } }
  - name: hot
    count: 3
    config: { node.roles: ["data_hot", "data_content", "ingest"] }
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          resources: { requests: { memory: 16Gi, cpu: 4 }, limits: { memory: 16Gi } }
    volumeClaimTemplates:
    - metadata: { name: elasticsearch-data }
      spec: { accessModes: [ReadWriteOnce], storageClassName: fast-ssd, resources: { requests: { storage: 1Ti } } }
```
The PVC template name must be `elasticsearch-data` unless you add a matching volume mount for the data path. Without a template ECK creates a 1Gi PVC per pod, which is too small for production.

## Access
```bash
kubectl -n search get secret prod-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
kubectl -n search port-forward svc/prod-es-http 9200
```

## Operations
- **Upgrade:** change `spec.version`; ECK does a rolling upgrade, which only makes progress while cluster health is green (documented exceptions exist).
- **Scale:** change `count`; before a node is removed ECK migrates its data to other nodes (with limitations, e.g. replica settings must allow it).
- **Storage growth:** increase the request in `volumeClaimTemplates` if the storage class allows volume expansion; otherwise create a new nodeSet and remove the old one.
- **vm.max_map_count:** set to `1048576` for Elasticsearch 8.16+ (`262144` for 8.15 and earlier) on the host, via a privileged init container or a DaemonSet; or set `node.store.allow_mmap: false` (documented as a fallback).

## Pitfalls
- Renaming a nodeSet makes ECK create a new nodeSet, migrate data away from the old one and then remove it.
- `volumeClaimDeletePolicy` defaults to `DeleteOnScaledownAndClusterDeletion`: PVCs are deleted together with the Elasticsearch cluster. Set `DeleteOnScaledownOnly` to keep them after cluster deletion.

## Verify
`kubectl -n search get elasticsearch` shows `HEALTH green` and `PHASE Ready`; `kubectl get pods -l elasticsearch.k8s.elastic.co/cluster-name=prod` all Running.

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (ECK docs; the install snippet uses a `version.eck` variable and the latest GitHub release is v3.5.0). Confirmed: crds.yaml/operator.yaml install URLs, `elasticsearch-data` volume claim name and the 1Gi default PVC, `volumeClaimDeletePolicy` values and default, vm.max_map_count values by Elasticsearch version, `<name>-es-elastic-user` secret, rename and scale-down data migration, green-health rule for rolling upgrades. Removed the pinned 2.14.0 and 8.15.3 versions (stale), the unconfirmed heap auto-sizing, master-order and local-PV claims. Zone allocation awareness advice was removed as unchecked.

Method: documentation only; no commands were run.
