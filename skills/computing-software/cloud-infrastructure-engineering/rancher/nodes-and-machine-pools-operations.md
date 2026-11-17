---
id: computing-software.cloud-infrastructure-engineering.rancher.nodes-and-machine-pools-operations
name: nodes-and-machine-pools-operations
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [nodes, machine-pools, cordon, drain, scale, auto-replace, ssh-key, registered-clusters]
level: practitioner
status: docs-checked
description: "Day-two node operations in Rancher: options per cluster type, scaling pools, delete versus scale down, SSH keys, hosted and registered limits."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/manage-clusters/nodes-and-machine-pools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Open a cluster with **Explore** and choose **Nodes**. What you can do depends on how the cluster was provisioned.

| Option | Infra-provider nodes | Custom | Hosted | Registered EKS | Other registered |
|---|---|---|---|---|---|
| Cordon, Drain, Edit, View API | yes | yes | yes | yes | yes |
| Delete | yes | yes | no | via View API | via View API |
| Download Keys | yes | no | no | no | no |
| Node Scaling | yes | no | no | yes | no |

Cordon marks a node unschedulable; Drain does that and evicts pods. Edit changes the name, description, labels and taints.

**Delete versus scale down.** Delete removes a defective node from the cloud provider. If the node is in a machine pool with auto-replace enabled, Rancher replaces it with an identically provisioned one. If you actually want fewer nodes, the page advises scaling down the pool instead of deleting. Scaling uses the scale controls on each machine pool and is only for nodes hosted by an infrastructure provider.

For clusters from hosted Kubernetes providers, node options are limited; edit the cluster itself rather than scaling in the Rancher UI. For registered clusters you can deploy workloads but cannot manage individual nodes, which must be handled outside Rancher.

To SSH into a provider-hosted node: open the cluster, **Machine Pools** tab, **Download SSH Key** from the node menu, extract the ZIP, and run `ssh -i id_rsa root@<IP_OF_HOST>` from that directory.

## Checked

2026-11-09. Read the cited Nodes and Machine Pools page in full and checked every claim against it (option table per cluster type, node actions, delete versus scale down, scaling, SSH key steps). No claims removed.

Method: documentation only; no commands were run.
