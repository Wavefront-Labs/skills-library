---
id: computing-software.cloud-infrastructure-engineering.external-dns.dnsendpoint-crd-source
name: dnsendpoint-crd-source
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, crd-source, dnsendpoint, managed-record-types, dname-record, annotation-filter]
level: practitioner
status: docs-checked
description: "Declare DNS records with the DNSEndpoint CRD source: flags, example A manifest, CNAME and DNAME notes, managed-record-types, annotation-filter gotcha and RBAC."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/crd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSEndpoint CRD source

Register the CRD, then enable the source:

```sh
kubectl apply --server-side=true -f "https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/config/crd/standard/dnsendpoints.externaldns.k8s.io.yaml"
external-dns --source crd --crd-source-apiversion externaldns.k8s.io/v1alpha1 --crd-source-kind DNSEndpoint --provider inmemory --policy sync --once --dry-run
```

```yaml
apiVersion: externaldns.k8s.io/v1alpha1
kind: DNSEndpoint
metadata:
  name: examplearecord
spec:
  endpoints:
  - dnsName: example.com
    recordTTL: 60
    recordType: A
    targets:
    - 10.0.0.1
```

- **Record types are not all enabled by default.** Pass `--managed-record-types=A --managed-record-types=CNAME --managed-record-types=NS` as needed.
- CNAME and DNAME targets accept bare or trailing-dot names; other types do not accept a trailing dot.
- `DNAME` redirects a whole subtree (`x.sub.example.com` is rewritten to `x.example.net`), while CNAME aliases one name. Only providers whose backend has DNAME work (NS1, OCI, PowerDNS, Scaleway, RFC2136 backends); Route 53, Azure, Google and Cloudflare reject it. Do not manage other records below a DNAME.
- **annotation-filter:** if set, the DNSEndpoint itself must carry the matching annotation, or it is ignored.
- Annotations other than that filter are not processed on DNSEndpoint objects.

RBAC:
```yaml
- apiGroups: ["externaldns.k8s.io"]
  resources: ["dnsendpoints"]
  verbs: ["get","watch","list"]
- apiGroups: ["externaldns.k8s.io"]
  resources: ["dnsendpoints/status"]
  verbs: ["*"]
```

## Checked

2026-11-04. Confirmed against the ExternalDNS CRD Source page: registering the CRD, usage flags, annotation-filter behaviour, record-types note, trailing-dot note, DNAME section and provider support, and the RBAC rules. Annotation-ignored point matches the configuration precedence page. Nothing removed.
Method: documentation only; no commands were run.
