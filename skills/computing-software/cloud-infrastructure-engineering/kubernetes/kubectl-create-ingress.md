---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-create-ingress
name: kubectl-create-ingress
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ingress, kubectl-create-ingress, ingressclass, kubectl-create]
level: practitioner
status: docs-checked
description: "Generate Ingress objects quickly with kubectl create ingress: rule syntax for host/path, pathType, TLS, class, annotations and default backend."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_ingress/", "https://kubernetes.io/docs/concepts/services-networking/ingress/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl create ingress

## Rule syntax
`--rule="host/path=service:port[,tls[=secret]]"`; a trailing `*` on the path means
`pathType: Prefix`, otherwise `Exact`.

```bash
kubectl create ingress web --class=nginx \
  --rule="shop.example.com/*=web:80" \
  --rule="shop.example.com/api/*=api:8080"

kubectl create ingress web --class=nginx \
  --rule="shop.example.com/*=web:80,tls=shop-tls"           # TLS with secret shop-tls

kubectl create ingress catch-all --class=nginx --default-backend=fallback:80

kubectl create ingress web --class=nginx --rule="/*=web:http" \
  --annotation nginx.ingress.kubernetes.io/rewrite-target=/ \
  --dry-run=client -o yaml > ingress.yaml
```
Port can be a number or a named Service port.

## Check the generated spec
```bash
kubectl get ingress web -o yaml
kubectl describe ingress web      # backends resolved to endpoints?
```
If `describe` shows a backend that does not resolve, check the Service name and port.

## Gotchas
- If `ingressClassName` is omitted, a default IngressClass should be defined; some controllers work without one, but the Kubernetes project recommends defining a default.
- `Exact` vs `Prefix`: `/api` Exact does not match `/api/users`. Use the `*` suffix.
- Wildcard hosts: `--rule="*.example.com/*=web:80"` (quote it so the shell does not glob).

## Checked
Checked 2026-10-24 against the kubectl create ingress source (main) and the Ingress documentation (v1.37): rule grammar `host/path=service:port[,tls[=secret]]`, trailing `*` makes pathType Prefix (otherwise Exact), `--class`, `--default-backend`, `--annotation`, wildcard hosts accepted by the rule pattern, Exact versus Prefix matching, default IngressClass wording. Removed the unconfirmed yq pipe, error text and TLS-namespace claim.
Method: documentation only; no commands were run.
