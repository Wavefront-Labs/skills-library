---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-remote-cluster-mode
name: opa-gatekeeper-remote-cluster-mode
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, remote-cluster, kubeconfig, management-cluster, hosted-control-plane, rbac, podstatus]
level: sme
status: docs-checked
description: "Run Gatekeeper in a management cluster while enforcing policy on a target cluster using --enable-remote-cluster and --kubeconfig (alpha)."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/customize-startup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper remote cluster mode

Remote cluster mode (alpha) suits hosted control plane designs where the target cluster API server runs inside a management cluster. Gatekeeper runs locally and enforces on a separate cluster:

```bash
--enable-remote-cluster
--kubeconfig=<kubeconfig for the target cluster>
```

Status resources (`ConstraintTemplatePodStatus` and the other pod status kinds) live on the management cluster next to the Gatekeeper pod, with OwnerReferences to the pod, so a pod restart garbage-collects its old status objects automatically.

Gatekeeper needs a Role on the management cluster named `gatekeeper-manager-role` in `gatekeeper-system`: `get` on `pods`, plus full verbs on `status.gatekeeper.sh` resources.

Migration: older versions stored status resources on the target cluster, which can leave orphans there. One-time cleanup:

```bash
kubectl delete constrainttemplatepodstatuses,constraintpodstatuses,mutatorpodstatuses,expansiontemplatepodstatuses,configpodstatuses,providerpodstatuses,connectionpodstatuses \
  -n gatekeeper-system --all --context <target-cluster-context>
```

To remove the statuses of one old pod only, select by label `gatekeeper.sh/pod=<old pod name>`. The separate Remote Cluster Mode guide covers CRDs on both clusters, webhook certificates and a smoke test.

## Checked

2026-11-04. Confirmed against customize-startup.md (Remote Cluster Mode for Gatekeeper). Removed or corrected: nothing.

Method: documentation only; no commands were run.
