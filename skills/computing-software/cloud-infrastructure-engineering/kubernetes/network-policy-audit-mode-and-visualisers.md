---
id: computing-software.cloud-infrastructure-engineering.kubernetes.network-policy-audit-mode-and-visualisers
name: network-policy-audit-mode-and-visualisers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, network-policy, policy-audit-mode, netpol-visualiser, cilium, hubble, calico, staged-policy]
level: practitioner
status: docs-checked
description: "Roll out NetworkPolicies without outages: run Cilium policy audit mode or Calico staged policies, read would-be drops in flow logs, and visualise policies before enforcing."
sources: ["https://docs.cilium.io/en/stable/security/policy-creation/", "https://docs.cilium.io/en/stable/observability/hubble/hubble-ui/", "https://docs.tigera.io/calico/latest/network-policy/staged-network-policies", "https://krew.sigs.k8s.io/plugins/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network policy audit mode and visualisers

## Why
Default-deny applied blind breaks DNS, metrics scraping and webhooks. Audit
mode lets you see what *would* be dropped while everything still flows. Core Kubernetes
NetworkPolicy has no way to log blocked or accepted connections (a limitation the Kubernetes docs
list), so this needs CNI features.

## Cilium: policy audit mode
Policy Audit Mode makes Cilium allow all traffic while logging the connections that network policies
would otherwise drop. The Cilium guide says it can be set for the whole daemon or for individual
endpoints, that no network policy is enforced while it is on (not recommended for production), and
that it audits layer 3 and 4 policies.

Cluster-wide, via the `cilium-config` ConfigMap, then restart the agents:
```bash
kubectl patch -n $CILIUM_NAMESPACE configmap cilium-config --type merge --patch '{"data":{"policy-audit-mode":"true"}}'
kubectl -n $CILIUM_NAMESPACE rollout restart ds/cilium
# or, for a Helm install: helm upgrade ... --reuse-values --set policyAuditMode=true
```
Per endpoint (run inside the Cilium agent pod on the endpoint's node):
```bash
kubectl -n $CILIUM_NAMESPACE exec $CILIUM_POD -c cilium-agent -- \
    cilium-dbg endpoint config $ENDPOINT PolicyAuditMode=Enabled
```
(`$ENDPOINT` is the endpoint ID from the pod's CiliumEndpoint `status.id`.)

Read would-be drops with the Hubble CLI, which has an `AUDIT` verdict filter:
```bash
hubble observe --verdict AUDIT --namespace shop
hubble observe flows -t policy-verdict          # shows "policy-verdict:none AUDITED" for would-be denies
```
Iterate until no unexpected AUDIT verdicts appear over a full business cycle (include cron jobs,
backups, month-end batch), then turn audit mode off (set `policy-audit-mode` back to `"false"` and
restart the agents, or unset it on the endpoint).

## Calico: staged policies
Calico Open Source documents staged policy resources that behave like their enforced counterparts:
`StagedNetworkPolicy`, `StagedGlobalNetworkPolicy` and `StagedKubernetesNetworkPolicy`
(the docs also list `StagedCalicoNetworkPolicy` for `CalicoNetworkPolicy`). They let you test the
traffic impact as if enforced without changing traffic flow. Their effect shows in the
`policies.pending` field of the flow logs in the Calico Whisker web console. To enforce, create an
identical enforced policy and apply it. A policy rule can also use `action: Log`; processing
continues with the next rule after a `Log` action.

## Visualisers
- **Hubble UI**: the Cilium graphical service map.
- **Calico Whisker**: the web console for Calico flow logs.
- A kubectl plugin installable through krew, `np-viewer` ("Network Policies rules viewer"), is
  published in the krew index.
- Policies generated from observed traffic are a starting point only; review them by hand.

## Rollout recipe
1. Enable audit for one namespace's endpoints.
2. Apply default-deny plus allows (DNS egress to the cluster DNS service, the ingress controller, the metrics scraper).
3. Watch AUDIT verdicts; add allows; repeat.
4. Disable audit; alert on `hubble observe --verdict DROPPED` for regressions.

## Gotchas
- Audit mode is a Cilium agent or endpoint setting: forgetting to turn it off means policies never enforce.
- Per the Cilium entities documentation, host-network traffic on the local node is the `host` entity and
  nodes in connected clusters are `remote-node`; use `fromEntities` for them in Cilium policies.

## Checked
Checked 2026-10-24 against the Cilium documentation sources (`security/policy-creation.rst`: audit
mode, ConfigMap key `policy-audit-mode`, Helm value `policyAuditMode`, endpoint option
`PolicyAuditMode`, `AUDITED` verdict; `hubble observe` help: `--verdict` values; `layer3.rst`:
`host`/`remote-node` entities; Hubble UI page), the Calico documentation sources (staged policy
resource names, `policies.pending`, rule actions incl. `Log`), the krew index entry for `np-viewer`
and the Kubernetes Network Policies page (no logging in core NetworkPolicy). Removed: `cilium config set`,
JSON/awk-style flow aggregation, Inspektor Gadget and the third-party policy-editor website, which
no checked documentation covers.
Method: documentation only; no commands were run.
