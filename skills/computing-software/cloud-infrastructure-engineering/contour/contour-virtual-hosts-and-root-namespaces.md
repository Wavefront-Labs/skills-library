---
id: computing-software.cloud-infrastructure-engineering.contour.contour-virtual-hosts-and-root-namespaces
name: contour-virtual-hosts-and-root-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [virtualhost, fqdn, root-namespaces, aliases, name-based-virtual-hosting, rbac]
level: practitioner
status: docs-checked
description: "HTTPProxy virtual hosts: one fqdn per root, converting multi-host Ingress, alias hosts via shared includes, restricting root HTTPProxy namespaces."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/virtual-hosts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Virtual hosts and root namespaces

HTTPProxy supports name-based virtual hosting but allows a single `fqdn` per root proxy. A multi-host Ingress must become one HTTPProxy per host.

Aliases: to serve the same routes under `bar.com` and `www.bar.com`, create two roots that include one shared non-root proxy:

```yaml
spec:
  virtualhost: {fqdn: bar.com}
  includes:
  - {name: main, namespace: default}
---
spec:
  virtualhost: {fqdn: www.bar.com}
  includes:
  - {name: main, namespace: default}
---
# kind HTTPProxy named main, no virtualhost:
spec:
  routes:
  - services: [{name: s2, port: 80}]
```

Restricting who can create roots: inclusion limits who controls routes for a domain, not where roots may live. Start Contour with `--root-namespaces=default,kube-system,my-admin-namespace`.
- A proxy with `virtualhost` outside those namespaces is flagged `invalid` and ignored.
- Contour then watches Secrets only in the listed root namespaces.
- Pair it with RBAC limiting Contour's access to the same namespaces (the repo has an `examples/root-rbac` sample creating a `root-httproxy` namespace).
- It affects HTTPProxy only, not Ingress; use `--watch-namespaces` to limit other resources.

## Checked

2026-11-08. Read the Contour main-branch config page virtual-hosts.md in full. Confirmed: name-based virtual hosting, one root domain per HTTPProxy, the Ingress conversion example, root proxy definition, the alias pattern through a shared include, and the `--root-namespaces` behaviour (invalid and ignored outside the list, Secret watching limited to those namespaces, RBAC advice, HTTPProxy only, `--watch-namespaces` for other resources). No claims removed.

Method: documentation only; no commands were run.
