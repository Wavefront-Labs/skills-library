---
id: computing-software.cloud-infrastructure-engineering.cert-manager.http01-solver
name: http01-solver
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [http01, ingressclassname, gatewayhttproute, acmesolver, podtemplate, servicetype]
level: practitioner
status: docs-checked
description: "Configure the cert-manager HTTP01 solver for Ingress and Gateway API: ingressClassName, class, name, serviceType, podTemplate and nameserver flags."
sources:
  - https://cert-manager.io/docs/configuration/acme/http01/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Network: your ingress controller or Gateway must reach the temporary `acmesolver` Pod and Service, and the API server must reach the cert-manager webhook. Default-deny NetworkPolicies can block either.

Ingress solver, `spec.acme.solvers[].http01.ingress`:
- `ingressClassName` (1.12+): recommended; creates new Ingresses. Not supported by ingress-gce. Per-Ingress override annotation `acme.cert-manager.io/http01-ingress-ingressclassname`.
- `class`: sets `kubernetes.io/ingress.class` on a randomly named Ingress; recommended only for ingress-gce.
- `name`: edits a named existing Ingress; avoid with controllers sharing one IP across Ingresses (annotation conflicts).
- If all three are unset, every installed controller may serve the solver.
- `serviceType`: `ClusterIP` or `NodePort`; unset defaults to `NodePort`.
- `podTemplate.spec` allows only `nodeSelector`, `tolerations`, `affinity`, `priorityClassName`, `serviceAccountName`, `securityContext`, `imagePullSecrets`, `resources`. Limits below the global requests make Kubernetes reject the Pod and the challenge fail.
- `ingressTemplate`: only metadata labels and annotations.

Gateway API, `http01.gatewayHTTPRoute` (beta in 1.15): needs the Gateway API CRDs and Helm `config.gatewayAPI.enabled=true`; install the CRDs first or run `kubectl rollout restart deployment cert-manager -n cert-manager`. `parentRefs`/`labels` select a Gateway with a port 80 listener. A temporary HTTPRoute `cm-acme-http-solver-*` is created. If `labels` match no Gateway, nothing happens and no error is raised.

Split-horizon DNS: `--acme-http01-solver-nameservers` takes comma-separated `host:port`; default is `/etc/resolv.conf`. In Helm, pass it through `extraArgs` and escape the comma as `\,` in `--set`.

## Checked

2026-11-03. Confirmed on the cert-manager HTTP01 page (configuration/acme/http01): network policy notes, ingressClassName (1.12), class, name, serviceType default, podTemplate allowed fields and limits caveat, ingressTemplate, Gateway API steps and beta state in 1.15, labels behaviour, nameserver flag. Fixed: the Helm comma escape is a single backslash in the page example, not two.
Method: documentation only; no commands were run.
