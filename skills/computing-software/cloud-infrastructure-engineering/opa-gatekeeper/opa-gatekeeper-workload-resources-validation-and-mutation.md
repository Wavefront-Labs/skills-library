---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-workload-resources-validation-and-mutation
name: opa-gatekeeper-workload-resources-validation-and-mutation
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, workload, deployment, pod, replicaset, violation-messages, podtemplatespec]
level: practitioner
status: docs-checked
description: "Understand why Pod constraints do not block Deployments, where denial messages appear, and how mutation behaves on workload resources."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/workload-resources.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper workload resources validation and mutation

Library constraints usually target Pods. A Deployment containing a privileged container is not blocked, because the constraint matches only Pods that pass admission. The Deployment controller later fails to create Pods; the denial message lands on the ReplicaSet status and eventually the Deployment status conditions.

Retrieve it:

```shell
kubectl get replicaset <name> -o jsonpath='{ .status.conditions[].message }'
kubectl get deploy <name> -o jsonpath='{ .status.conditions[*].message }'
```

Simply adding Deployment to a library constraint `kinds` list will not work: the Rego reads `spec.containers[_]` (and `initContainers`), whereas workloads nest it at `spec.template.spec.containers[_]`. To reject the workload itself, use the ExpansionTemplate feature (v3.10+).

Mutation: a mutator on a workload PodTemplateSpec implicitly mutates the Pods it creates, whereas a mutation on individual Pods does not propagate back to the parent. Use the mutator extent-of-changes section (`applyTo` and `match`) to decide which level to target.

## Checked

2026-11-08: read the whole of website/docs/workload-resources.md in the Gatekeeper repo. Confirmed every claim, including the kubectl commands, the Rego field paths and the v3.10+ expansion feature; nothing removed.

Method: documentation only; no commands were run.
