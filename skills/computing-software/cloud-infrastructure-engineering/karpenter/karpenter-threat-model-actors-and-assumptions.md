---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-threat-model-actors-and-assumptions
name: karpenter-threat-model-actors-and-assumptions
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [threat-model, security, actors, rbac, iam, irsa, nodepool-limits]
level: advanced
status: docs-checked
description: "Karpenter threat model actors (operator, developer, controller), assumptions, and the node-count threat mitigated with NodePool limits and resource quotas."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/threat-model.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter threat model: actors and assumptions

Actors:
1. Cluster Operator: installs Karpenter, owns NodePools, EC2NodeClasses and the cloud identities and permissions for nodes and the controller.
2. Cluster Developer: creates pods through Deployments, Jobs, StatefulSets and so on; assumed unable to modify the Karpenter pod or use its service account.
3. Karpenter Controller: creates and removes instances and nodes, evicts pods. Its Kubernetes RBAC lives in the helm chart (aggregate-clusterrole, clusterrole-core, clusterrole, role, rolebinding).

Assumptions the model relies on:
- Karpenter runs on a cluster node and authenticates via a service account.
- Developers have no Kubernetes permissions on the Karpenter deployment, pods or clusterroles.
- Restricting pod fields developers may set is out of scope; use a policy framework.
- No sensitive data sits in non-Secret resources, because Karpenter can list pods, nodes, deployments and storage types. It cannot list or watch cluster-wide ConfigMaps/Secrets.
- Karpenter may create, modify and delete nodes and evict any pod. The page suggests operators running workloads with varying security profiles in one cluster may want dedicated nodes and scheduling rules for Karpenter, and a system-pool for the Karpenter pod, to mitigate container escapes.
- AWS: the Karpenter IAM policy is the one encoded in the GitHub repo (extra permissions granted by the administrator are out of scope) and the pod uses IRSA for AWS credentials (IRSA setup is out of scope).

Threat: a developer forces many nodes (many pods, or anti-affinity of one pod per node). Mitigate with Kubernetes object-count resource quotas plus `spec.limits` on each NodePool, which limit the total memory, CPU or other resources provisioned across all nodes.

## Checked

2026-11-08. Confirmed against the Threat model reference (v1.13): actors, capabilities, assumptions table and the node-count threat. Removed the unsupported mention of Pod Identity and the "isolate accordingly" advice, replaced with the page's wording.

Method: documentation only; no commands were run.

