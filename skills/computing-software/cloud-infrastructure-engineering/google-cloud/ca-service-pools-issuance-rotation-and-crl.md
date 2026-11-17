---
id: computing-software.cloud-infrastructure-engineering.google-cloud.ca-service-pools-issuance-rotation-and-crl
name: ca-service-pools-issuance-rotation-and-crl
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, certificate-authority-service, ca-pool-create, gcloud-privateca, issue-certificate, gcloud-privateca-certificates-create, ca-rotation, ca-disable, cas-iam, certificate-requester, crl-publishing, cas-publishing]
level: advanced
status: docs-checked
description: "Run a private PKI on CA Service: create pools and root/subordinate CAs with gcloud privateca, issue certificates, rotate and disable CAs, publish CRLs, and split IAM roles."
sources: ["https://cloud.google.com/certificate-authority-service/docs/creating-ca-pool", "https://cloud.google.com/certificate-authority-service/docs/creating-certificate-authorities", "https://cloud.google.com/certificate-authority-service/docs/requesting-certificates", "https://cloud.google.com/certificate-authority-service/docs/rotate-ca", "https://cloud.google.com/certificate-authority-service/docs/reference/permissions-and-roles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CA Service: pools, issuance, rotation and CRLs

## 1. Pools and CAs
```bash
gcloud privateca pools create root-pool --location=europe-west2 --tier=enterprise --publish-ca-cert --publish-crl
gcloud privateca roots create root-2026 --pool=root-pool --location=europe-west2 \
  --subject="CN=Example Internal Root 2026, O=Example Ltd" --key-algorithm=ec-p384-sha384 \
  --max-chain-length=1 --validity=P10Y --auto-enable
gcloud privateca pools create issuing-pool --location=europe-west2 --tier=devops   # high volume, short-lived, no CRL
gcloud privateca subordinates create issuing-2026a --pool=issuing-pool --location=europe-west2 \
  --issuer-pool=root-pool --issuer-location=europe-west2 \
  --subject="CN=Example Issuing CA 2026a, O=Example Ltd" --key-algorithm=ec-p256-sha256 --validity=P3Y --auto-enable
```
Tier (default Enterprise when unspecified): the choice affects whether CA Service stores issued certificates, whether they can be revoked,
and the maximum certificate creation rate. Only Enterprise pools support revocation and CRL publication; DevOps suits high-volume, short-lived certificates.
Constrain issuance with a pool issuance policy or certificate templates.

## 2. Issue
```bash
gcloud privateca certificates create --issuer-pool=issuing-pool --issuer-location=europe-west2 \
  --generate-key --key-output-file=svc.key --cert-output-file=svc.crt \
  --dns-san=orders.internal.example.com --validity=P30D
# or from a CSR
gcloud privateca certificates create --issuer-pool=issuing-pool --issuer-location=europe-west2 --csr=svc.csr --cert-output-file=svc.crt
```
`--validity` is optional; the default is 30 days.

## 3. Rotate and disable
A pool issues from any **enabled** CA in it. Rotation:
1. Create the new CA in the same pool (`issuing-2027a`), enabled.
2. Distribute the new chain to trust stores (if under the same root, nothing to do).
3. `gcloud privateca subordinates disable issuing-2026a --pool=issuing-pool --location=<R>` — stops issuing; existing certs stay valid.
4. Delete it only after its last certificate expires.

## 4. Revocation and CRL
```bash
gcloud privateca certificates revoke --certificate=<CERT_ID> --issuer-pool=root-pool --issuer-location=<R> --reason=key_compromise
```
With CRL publication enabled (default when creating the pool with gcloud or the console; Enterprise tier only) CRLs and CA certificates go to a Cloud Storage bucket
(`--bucket` for your own) and the URLs are embedded in issued certificates (CDP, AIA); certificates issued while publication was off lack the extension. A new CRL is published daily and is valid for 7 days, and
another within 15 minutes of a revocation. A CRL holds at most 500,000 unexpired revoked certificates; the last 100 CRLs are kept as resources. A root CA's CRL covers only the certificates it issued, not itself.
Revocation works only if clients download CRLs and reject listed serial numbers.

## 5. IAM split
| Role | Who |
|---|---|
| `roles/privateca.admin` / `caManager` (Operation Manager) | PKI admins only (create pools and CAs, revoke) |
| `roles/privateca.certificateRequester` or `certificateManager` | workloads/cert-manager |
| `roles/privateca.workloadCertificateRequester` | certificates with the caller's identity |

## Gotchas
- Only Enterprise pools can revoke; do not put roots in a DevOps pool if you need revocation.
- Test issuance policy changes in a separate pool first.
- CRL publishing doesn't help clients that don't check CRLs; short lifetimes are the practical revocation.

## Verify
- [ ] `openssl verify -CAfile chain.pem svc.crt` succeeds; `openssl x509 -in svc.crt -noout -ext crlDistributionPoints` shows the CRL URL (Enterprise).
- [ ] A requester without the role gets PERMISSION_DENIED.

## Checked
Date: 2026-10-28. Confirmed against the CA Service pages (Creating a CA pool, Creating certificate authorities, Requesting certificates, Revoking certificates, Permissions and roles): tiers and default, Enterprise-only revocation and CRL, publication defaults, daily CRL with 7-day validity and 15-minute out-of-band CRL, 500,000 and 100-CRL limits, `--bucket`, 30-day default validity, role names; gcloud flags checked against the CLI reference. Removed: HSM-backed root claim, undelete grace period, cert-manager/mesh integrations, the auditor role, and the "no stored certificates" wording. Subjects, hostnames and pool names are examples.
Method: documentation only; no commands were run.
