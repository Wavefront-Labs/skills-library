---
id: computing-software.cloud-infrastructure-engineering.kubernetes.tenant-fair-sharing-kueue-apf
name: tenant-fair-sharing-kueue-apf
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-tenancy-isolation, fair-sharing, kueue, api-priority-and-fairness, flowschema]
level: practitioner
status: docs-checked
description: "Share batch capacity fairly between tenants with Kueue cohorts, borrowing limits and fair-sharing weights, and protect the API server with per-tenant APF flow schemas."
sources: ["https://kueue.sigs.k8s.io/docs/concepts/fair_sharing/", "https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/", "https://kueue.sigs.k8s.io/docs/concepts/cohort/", "https://kueue.sigs.k8s.io/docs/concepts/preemption/", "https://kubernetes.io/docs/concepts/cluster-administration/flow-control/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fair sharing across tenants

## Compute: Kueue cohorts
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata: {name: team-a}
spec:
  cohortName: research
  namespaceSelector: {matchLabels: {tenant: a}}
  fairSharing: {weight: "2"}             # gets twice the share of weight-1 queues when contended
  preemption:
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
  resourceGroups:
  - coveredResources: [cpu, memory, nvidia.com/gpu]
    flavors:
    - name: default
      resources:
      - {name: cpu, nominalQuota: 100, borrowingLimit: 50, lendingLimit: 20}
      - {name: memory, nominalQuota: 400Gi}
      - {name: nvidia.com/gpu, nominalQuota: 4, borrowingLimit: 4}
```
Idle quota is borrowed by others in the cohort; when the owner needs it back, Kueue preempts
borrowed workloads. Fair sharing is turned on in the Kueue `Configuration` (`config.kueue.x-k8s.io/v1beta2`) by adding a
`fairSharing` section, for example `preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]`;
Kueue then weights each ClusterQueue's share by `.spec.fairSharing.weight`.

## API server: APF per tenant
Without it, one tenant's controllers or scripts can starve everyone's API requests.
```yaml
apiVersion: flowcontrol.apiserver.k8s.io/v1
kind: PriorityLevelConfiguration
metadata: {name: tenants}
spec:
  type: Limited
  limited:
    nominalConcurrencyShares: 20
    limitResponse: {type: Queue, queuing: {queues: 64, handSize: 6, queueLengthLimit: 50}}
---
apiVersion: flowcontrol.apiserver.k8s.io/v1
kind: FlowSchema
metadata: {name: tenant-serviceaccounts}
spec:
  priorityLevelConfiguration: {name: tenants}
  matchingPrecedence: 5000
  distinguisherMethod: {type: ByNamespace}   # fair queuing per tenant namespace
  rules:
  - subjects: [{kind: Group, group: {name: system:serviceaccounts}}]
    resourceRules: [{verbs: ["*"], apiGroups: ["*"], resources: ["*"], namespaces: ["*"]}]
```

## Verify
```bash
kubectl get clusterqueue team-a -o jsonpath='{.status.fairSharing.weightedShare}'
kubectl get --raw /metrics | grep apiserver_flowcontrol_rejected_requests_total | grep tenants
```

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026; Kueue docs (main)
- Corrected the Kueue API: current docs use `kueue.x-k8s.io/v1beta2` and `spec.cohortName` (Cohort page); fair sharing is enabled by a `fairSharing` section with `preemptionStrategies` in the Kueue Configuration, not `fairSharing.enable`; confirmed `.spec.fairSharing.weight` and `.status.fairSharing.weightedShare` and the `reclaimWithinCohort`, `withinClusterQueue`, `borrowingLimit` and `lendingLimit` fields (preemption and ClusterQueue pages).
- Confirmed in the Kubernetes API types and flow-control page the `flowcontrol.apiserver.k8s.io/v1` kinds, `nominalConcurrencyShares`, `limitResponse`, FlowSchema `distinguisherMethod` (`ByUser` or `ByNamespace`), `matchingPrecedence`, and the metric `apiserver_flowcontrol_rejected_requests_total`.

Method: documentation only; no commands were run.
