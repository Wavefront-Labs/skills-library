---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.helm-chart-three-node-s3
name: helm-chart-three-node-s3
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [values-yaml, kubernetes, replicationplacement, helm]
level: practitioner
status: docs-checked
description: "Install SeaweedFS on Kubernetes with the Helm chart: a three-master, three-volume, two-filer, two-S3 recipe with replication 001 and a bucket."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Helm-Chart-Recipes
  - https://github.com/seaweedfs/seaweedfs/wiki/Deployment-to-Kubernetes-and-Minikube
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# helm chart three node s3

```bash
helm repo add seaweedfs https://seaweedfs.github.io/seaweedfs/helm
helm install seaweedfs seaweedfs/seaweedfs -n seaweedfs --create-namespace -f values.yaml
```
`values.yaml` for a 3-node S3 cluster:
```yaml
global:
  seaweedfs:
    enableReplication: true
    replicationPlacement: "001"
master:
  replicas: 3
  data: {type: persistentVolumeClaim, size: 1Gi}
volume:
  replicas: 3          # at least 1 + sum of the replication digits
  dataDirs:
    - {name: data, type: persistentVolumeClaim, size: 500Gi, maxVolumes: 0}
filer:
  replicas: 2
  data: {type: persistentVolumeClaim, size: 20Gi}
s3:
  enabled: true
  replicas: 2
  enableAuth: true
  credentials:
    admin: {accessKey: admin, secretKey: change-me}
  createBuckets:
    - name: app-storage
```
Three masters give Raft failover; `001` stores each write twice. Change the secret before use.

Alternative: the SeaweedFS Operator (`helm repo add seaweedfs-operator https://seaweedfs.github.io/seaweedfs-operator/helm`) with a `Seaweed` custom resource.

Verify: `kubectl -n seaweedfs get pods` all Running, then S3 `ls` through the service.

## Checked
Checked 2026-11-09: the two helm commands, the full three-node values block, the replicationPlacement digits and volume.replicas minimum, and the operator chart repository and Seaweed custom resource match the pages. Nothing removed.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Helm-Chart-Recipes (read in full) and Deployment-to-Kubernetes-and-Minikube (searched for the operator repository and Seaweed resource), from a local clone of the wiki.
