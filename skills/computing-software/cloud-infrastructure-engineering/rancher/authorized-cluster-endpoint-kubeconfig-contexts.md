---
id: computing-software.cloud-infrastructure-engineering.rancher.authorized-cluster-endpoint-kubeconfig-contexts
name: authorized-cluster-endpoint-kubeconfig-contexts
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [authorized-cluster-endpoint, ace, kubeconfig, kube-api-auth, fqdn, kubectl, contexts]
level: advanced
status: docs-checked
description: "Reach a downstream RKE2 or K3s cluster directly with the authorized cluster endpoint: extra kubeconfig contexts, the kube-api-auth webhook, and FQDN contexts."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/manage-clusters/access-clusters/authorized-cluster-endpoint
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/manage-clusters/access-clusters/use-kubectl-and-kubeconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Download a cluster's kubeconfig from **Cluster Management** via the row menu **Download KubeConfig**; each cluster has its own file. kubectl reads `~/.kube/config` by default, or any path given with `--kubeconfig`. If admins turned off kubeconfig token generation, the file needs the Rancher CLI on your PATH.

The authorized cluster endpoint (ACE) lets kubectl reach a Rancher-launched cluster **without** authenticating through the Rancher server. It is available for RKE2 and K3s clusters, where you must enable it manually. The page recommends setting it up as a best practice so that you can still reach the cluster if Rancher is down.

When enabled, the downloaded kubeconfig contains extra contexts. List them:

```
kubectl config get-contexts --kubeconfig /custom/path/kube.config
CURRENT   NAME                        CLUSTER                     AUTHINFO     NAMESPACE
*         my-cluster                  my-cluster                  user-46tmn
          my-cluster-controlplane-1   my-cluster-controlplane-1   user-46tmn
```

The first context authenticates through Rancher; the second talks to the downstream cluster directly. If an FQDN is defined for the cluster, a single context named `<CLUSTER_NAME>-fqdn` is created, used as `kubectl --context <CLUSTER_NAME>-fqdn get nodes`. The page recommends fronting ACE with a load balancer.

Mechanism: the `kube-api-auth` microservice authenticates direct requests. During provisioning `/etc/kubernetes/kube-api-authn-webhook.yaml` is deployed and `kube-apiserver` is configured with `--authentication-token-webhook-config-file=/etc/kubernetes/kube-api-authn-webhook.yaml`, so it queries `http://127.0.0.1:6440/v1/authenticate` for bearer tokens. Its scheduling rules keep it off Windows nodes and on control plane nodes.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: How the Authorized Cluster Endpoint Works; Access a Cluster with Kubectl and kubeconfig. Nothing removed.

Method: documentation only; no commands were run.
