---
id: computing-software.devops-ci-cd.argo-cd.rotating-cluster-credentials
name: rotating-cluster-credentials
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, cluster-credential-rotation, cluster-secrets, argocd-manager]
level: advanced
status: docs-checked
description: "Rotate credentials Argo CD uses for managed clusters: argocd cluster rotate-auth for the argocd-manager token, declarative cluster secrets, cloud IAM and cert expiry."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/security/#cluster-rbac", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_cluster_rotate-auth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rotating cluster credentials

## argocd-manager service account token
For clusters added with `argocd cluster add`, Argo uses the bearer token of the `argocd-manager` ServiceAccount, stored in a cluster secret in the `argocd` namespace.
```bash
argocd cluster rotate-auth https://prod.example.com:6443
```
The command takes a server URL or a cluster name (`argocd cluster rotate-auth SERVER/NAME`). Rotate on a schedule and when staff with access leave.

## Declarative cluster secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cluster-prod
  namespace: argocd
  labels: { argocd.argoproj.io/secret-type: cluster }
stringData:
  name: prod
  server: https://prod.example.com:6443
  config: |
    { "bearerToken": "<new token>", "tlsClientConfig": { "caData": "<base64 CA>" } }
```
Rotate by updating the secret, for example through an external secrets operator.

## Prefer short-lived auth
Where your cloud supports it, prefer short-lived or workload-identity based cluster auth over static bearer tokens; see the declarative cluster setup docs for the supported `config` options.

## Cert and CA changes
A cluster CA rotation invalidates the CA data stored in the cluster secret: update it before the old CA is removed.

## Verify
- [ ] Argo CD shows the cluster connection as successful and the old token no longer works.

## Checked
2026-10-28. Confirmed on the rotate-auth command reference: `argocd cluster rotate-auth SERVER/NAME` with a server URL or cluster name. Confirmed on the security and FAQ pages: the cluster secret in the `argocd` namespace carries the bearer token of the `argocd-manager` ServiceAccount created by `argocd cluster add`, and cluster secrets use the label `argocd.argoproj.io/secret-type: cluster`.
Removed (not confirmed): what rotate-auth does step by step and its kubeconfig requirement, the Kubernetes 1.24 token secret statement, `awsAuthConfig`, `execProviderConfig` and `argocd-k8s-auth` details, the x509 symptom and the `kubectl --token` test.

Method: documentation only; no commands were run.
