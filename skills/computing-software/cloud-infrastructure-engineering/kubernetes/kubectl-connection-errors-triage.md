---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-connection-errors-triage
name: kubectl-connection-errors-triage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-troubleshooting, kubectl-connection-refused, unauthorized-401, kubeconfig-contexts]
level: practitioner
status: docs-checked
description: "Decode kubectl connection failures: localhost:8080 refused, connection refused or timeout on 6443, unknown authority, Unauthorized and Forbidden, step by step."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/", "https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/", "https://kubernetes.io/docs/reference/kubectl/quick-reference/#kubectl-output-verbosity-and-debugging", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/#authenticating-api-requests", "https://kubernetes.io/docs/reference/using-api/health-checks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl connection errors

| Error | Meaning | Check |
|---|---|---|
| `The connection to the server localhost:8080 was refused - did you specify the right host or port?` | no kubeconfig found; kubectl fell back to the default `http://localhost:8080` | `echo $KUBECONFIG; ls ~/.kube/config`; on control planes `export KUBECONFIG=/etc/kubernetes/admin.conf` |
| `dial tcp 10.0.0.10:6443: connect: connection refused` | host reachable, nothing listening | apiserver down (crictl on control plane) or LB backend empty |
| `dial tcp ...:6443: i/o timeout` | packets dropped | firewall, security group, VPN, wrong IP |
| `x509: certificate signed by unknown authority` | CA in kubeconfig does not match server cert | wrong cluster/context, or TLS-intercepting proxy; set `HTTPS_PROXY`/`NO_PROXY` correctly |
| `x509: certificate is valid for ..., not <name>` | connecting via a name not in apiserver SANs | add SAN or use listed name |
| `x509: certificate has expired or is not yet valid` | server or client cert expired, or clock skew | `kubeadm certs check-expiration`, `date` |
| `error: You must be logged in to the server (Unauthorized)` | credentials rejected | expired client cert, expired OIDC token or exec plugin failing |
| `Error from server (Forbidden)` | authenticated, not authorised | RBAC, not connectivity |
| exec plugin reports an unsupported `client.authentication.k8s.io` apiVersion | kubeconfig written by an old cloud CLI (the authentication docs describe `v1` and `v1beta1`) | update the aws/gcloud/az CLI and regenerate the kubeconfig |

## Workflow
```bash
kubectl config current-context
kubectl config view --minify            # server URL, user, auth method
kubectl cluster-info -v=6               # shows requests and responses
curl -k https://<server>:6443/readyz    # reachability; answers without credentials only if default RBAC (system:public-info-viewer) and anonymous auth are in place
kubectl auth whoami                     # who am I, if auth works
```
`-v=7` displays HTTP request headers and `-v=8` displays HTTP request contents.

## Proxies
If a proxy sits between kubectl and the API server, put the cluster endpoint in `NO_PROXY`
(including the IP and the service CIDR for in-cluster tools).

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- kubectl messages `The connection to the server <host> was refused - did you specify the right host or port?`,
  `error: You must be logged in to the server (<reason>)` and `Error from server (<reason>)`: kubectl `helpers.go` v1.37.1;
  default server `http://localhost:8080` when no kubeconfig: client-go `client_config.go` v1.37.1.
- `-v` levels (6 requested resources, 7 request headers, 8 request contents): kubectl quick reference.
- `kubectl auth whoami` exists: authentication page. `kubeadm certs check-expiration` and one-year client certificates:
  kubeadm certificate management page. `export KUBECONFIG=/etc/kubernetes/admin.conf`: kubeadm create-cluster page.
- `/readyz` and the default `system:public-info-viewer` binding for unauthenticated users: API health-check and RBAC pages.
- Exec credential plugin apiVersions documented are `client.authentication.k8s.io/v1` and `v1beta1`.
- Removed: the quoted `v1alpha1` exec error text, the claim that `-v=8` shows headers and that corporate proxies break mTLS
  and watches, which the docs do not support.

Method: documentation only; no commands were run.
