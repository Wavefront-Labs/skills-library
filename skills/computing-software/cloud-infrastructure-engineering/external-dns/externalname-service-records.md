---
id: computing-software.cloud-infrastructure-engineering.external-dns.externalname-service-records
name: externalname-service-records
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, externalname-service, cname-record, externalname-ip, hostname-annotation-multi]
level: intro
status: docs-checked
description: "ExternalName Services in ExternalDNS: hostname annotation creates CNAMEs to externalName, or A records when externalName is an IP address."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/externalname.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExternalName Services

Use case from the docs: a subdomain that should point at an external domain, so a CNAME makes sense.

**Setup.** Run ExternalDNS with `--source=service`; the docs example also enables `--source=ingress`, `--namespace=dev`, `--domain-filter=example.org.`, `--registry=txt`, `--txt-owner-id=dev.example.org` and `--policy=upsert-only`.

**CNAME (default).** One annotation lists several hostnames, comma separated:
```yaml
kind: Service
apiVersion: v1
metadata:
  name: aws-service
  annotations:
    external-dns.kubernetes.io/hostname: tenant1.example.org,tenant2.example.org
spec:
  type: ExternalName
  externalName: aws.example.org
```
This creates CNAMEs `tenant1.example.org` and `tenant2.example.org` pointing to `aws.example.org`.

**IP address.** If `externalName` is an IP address, ExternalDNS creates **A records** instead of CNAMEs, for example `externalName: 111.111.111.111`.

Notes
- `upsert-only` prevents ExternalDNS deleting records; `--policy=sync` enables full synchronization including deletions.

## Checked

2026-11-04. Confirmed against the ExternalDNS ExternalName Services tutorial: use case, example flags, CNAME and A-record behaviour, upsert-only comment. Nothing removed.
Method: documentation only; no commands were run.
