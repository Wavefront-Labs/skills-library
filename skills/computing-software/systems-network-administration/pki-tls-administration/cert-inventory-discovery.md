---
id: computing-software.systems-network-administration.pki-tls-administration.cert-inventory-discovery
name: cert-inventory-discovery
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cert-inventory-discovery, pki-lifecycle, certificate-inventory, discovery, ct-search, network-scan, pki-tls-administration]
level: practitioner
status: draft
description: "Build a complete certificate inventory from network scans, CT logs, cloud APIs and key stores, with owners and renewal method."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
  - https://crt.sh/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certificate inventory and discovery
Goal: no certificate is unknown, ownerless or manually renewed by surprise.
Sources:
1. Network scan: `nmap -p 443,8443,636,993,995 --script ssl-cert 10.0.0.0/16` or `zmap` plus `openssl s_client`.
2. CT logs for public names (see CT monitoring).
3. Cloud: `aws acm list-certificates`, `aws iam list-server-certificates`, Azure Key Vault `az keyvault certificate list`, GCP Certificate Manager.
4. Stores: Windows `Get-ChildItem Cert:\LocalMachine\My -Recurse`, Java keystores, `/etc/ssl`, Kubernetes `kubectl get secret -A --field-selector type=kubernetes.io/tls`.
5. CA databases: `certutil -view` (AD CS), EJBCA reports.
Record: subject/SAN, issuer, serial, notAfter, key type, location, owner, renewal method (ACME, API, manual), environment.
Store in a CMDB or simple CSV with a nightly refresh job.
Gotcha: internal TLS ports on odd numbers (8443, 9443, 10250) hide expiring certs; scan wide, not only 443.
Verify:
- [ ] Count of certs seen by scan matches CA issuance records for the last 90 days.
- [ ] Every row has an owner and a renewal method.
