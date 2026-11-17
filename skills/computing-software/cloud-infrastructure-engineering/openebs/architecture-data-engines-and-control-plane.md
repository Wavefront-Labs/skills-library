---
id: computing-software.cloud-infrastructure-engineering.openebs.architecture-data-engines-and-control-plane
name: architecture-data-engines-and-control-plane
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [architecture, data-engine, control-plane, csi, operators, helm, custom-resources]
level: practitioner
status: docs-checked
description: "Map OpenEBS into data engines (volume access, services, data and storage layers) and the control plane (Helm, CRDs, operators, CSI driver, plugins, kubectl)."
sources:
  - https://openebs.io/docs/concepts/architecture
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OpenEBS splits into two groups: data engines and the control plane.

Data engines serve reads and writes to the storage. They aggregate block-device capacity into volumes, expose local or NVMe transports, and provide synchronous replication, snapshots, compression and encryption. Their layers are the volume access layer (POSIX through the CSI node driver or kubelet, with ext4/xfs or raw block), the volume services layer, the volume data layer and the storage layer (devices or directories, outside OpenEBS's scope). OpenEBS creates one controller, called the Target or Nexus, per volume, pinned to a specific list of nodes that each hold the full data via synchronous replication. Local Storage exposes device or directory paths; Replicated Storage exposes an NVMe target.

The control plane is a set of microservices managed by Kubernetes, with configuration saved as custom resources. Its parts:

- **Helm chart** installs components with Deployments, DaemonSets and StatefulSets and loads the CRDs. Control plane components are stateless and rely on custom resources and etcd.
- **Declarative API** exposed as CRDs, validated by CRD validators and admission webhooks.
- **Data engine operators**, cluster-scoped or node-level.
- **CSI driver** controlled by StorageClass parameters.
- **Plugins** for Velero, Prometheus/Grafana, logging stacks and policy tools.
- **CLI**: everything works through `kubectl`, plus an alpha-version kubectl plugin that aggregates pool and volume information.

Provisioned data engine pods run in the `openebs` namespace.

## Checked

Method: 2026-11-08 read the raw markdown of the cited architecture page in full and compared each claim; all are supported and unchanged except that the kubectl plugin is now noted as alpha, as the page states.
