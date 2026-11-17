---
id: computing-software.cloud-infrastructure-engineering.istio.istio-multicluster-primary-remote
name: istio-multicluster-primary-remote
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, multicluster, remote-secret, east-west-gateway]
level: practitioner
status: docs-checked
description: "Join clusters with shared root CA and remote secrets using istioctl create-remote-secret, and check east-west gateway reachability."
sources: ["https://istio.io/latest/docs/setup/install/multicluster/primary-remote/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In primary-remote, cluster1 runs the control plane and cluster2 is a remote cluster that uses it. The control plane in cluster1 observes the API servers of both clusters for endpoints, workloads communicate pod-to-pod across clusters, and cluster2 reaches the control plane through a dedicated east-west gateway in cluster1.

Cluster1 is installed with `values.global.externalIstiod: true`, `meshID`, `multiCluster.clusterName` and `network`. Cluster2 gets `topology.istio.io/controlPlaneClusters=cluster1` as an annotation on its `istio-system` namespace and is installed with `profile: remote` pointing at the east-west gateway address. Then attach cluster2 by giving cluster1 access to its API server:

```sh
istioctl create-remote-secret --context="${CTX_CLUSTER2}" --name=cluster2 | kubectl apply -f - --context="${CTX_CLUSTER1}"
```

Gotchas: the guide says these instructions are not suitable for an AWS EKS primary cluster, because AWS load balancers are FQDNs while the remote cluster uses an `ExternalName` Service that only supports IP addresses. The east-west gateway is public on the Internet by default, so production systems may need extra access restrictions such as firewall rules. The `remote` profile for the Helm charts needs Istio 1.24 or later. The `injectionPath` and `remotePilotAddress` settings are for demonstration; production should configure `injectionURL` with properly signed DNS certificates.

Verify: after the remote secret is applied, cluster1's control plane authenticates workloads from cluster2 and discovers endpoints there, so a service deployed in both clusters receives traffic in each.

## Checked

2026-11-03. Confirmed in the Istio primary-remote install guide: topology, `externalIstiod`, the `controlPlaneClusters` annotation, `profile: remote`, `istioctl create-remote-secret --name`, the EKS limitation, the east-west gateway exposure warning, the Helm 1.24 remark and the production `injectionURL` advice. Removed: `istioctl remote-clusters`, the common-root-CA and certificate-error claims (that is the multi-primary shape, not on this page), the remote-secret handling advice, the firewall port remark, the same-name-and-namespace rule and the failover drill.

Method: documentation only; no commands were run.
