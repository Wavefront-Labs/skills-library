---
id: computing-software.cloud-infrastructure-engineering.external-dns.crd-registry-dnsrecord
name: crd-registry-dnsrecord
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, crd-registry, dnsrecord, programmed-status, crd-registry-namespace]
level: advanced
status: docs-checked
description: "The alpha CRD registry stores ownership as DNSRecord custom resources: install, RBAC, flags, the Ready status lifecycle and its out-of-band blind spot."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/crd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD registry (alpha)

The docs mark it early and alpha: the `DNSRecord` API (`externaldns.k8s.io/v1alpha1`) may change incompatibly and it is not recommended for production.

Each managed endpoint is a `DNSRecord` object, viewable with `kubectl get dnsrecords`.

**It records what ExternalDNS applied, not a mirror of the provider.** Records changed out of band in the provider are not reconciled. Only records that reached `Programmed` count as current state.

**Setup**
- Helm: `registry: crd` and `txtOwnerId: my-identifier` install the CRD and RBAC.
- Manual: `kubectl apply -f config/crd/standard/dnsrecords.externaldns.k8s.io.yaml`.
- RBAC: a Role in the registry namespace with get, list, watch, create, update, delete on `dnsrecords`, and get, update on `dnsrecords/status`, bound to the ExternalDNS ServiceAccount.

**Flags**
```sh
--registry=crd
--txt-owner-id=my-identifier   # unique per deployment, stable for its lifetime
--crd-registry-namespace=external-dns
```
Without the namespace flag it uses the namespace ExternalDNS runs in, falling back to `default` outside a cluster. It is independent of `--namespace`.

**Status:** `status.conditions[type=Ready]` reason `Accepted` (planned, not yet programmed), `Programmed` (applied), `Failed` (provider rejected). A provider reports a single batch error, so every record in a failed batch is marked `Failed`; those actually applied are corrected to `Programmed` on the next reconcile.

**Limitation:** only the in-cluster Kubernetes API is supported.

## Checked

2026-11-04. Read the CRD registry page. Confirmed the alpha warning, the v1alpha1 API, kubectl get dnsrecords, the Helm values, the CRD manifest path, the RBAC rules, the three flags and namespace fallback, the Accepted/Programmed/Failed lifecycle and the in-cluster-only limitation. Removed nothing.

Method: documentation only; no commands were run.
