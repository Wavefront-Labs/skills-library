---
id: computing-software.cloud-infrastructure-engineering.google-cloud.certificate-authority-service-private-pki
name: certificate-authority-service-private-pki
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, certificate-authority-service, cas, private-ca, private-pki, ca-pools, root-ca, subordinate-ca, certificate-templates, issuance-policy, devops-tier, enterprise-tier, crl, ocsp, cert-manager-google-cas-issuer, workload-certificates, mtls-certificates, hsm-ca-keys, certificate-revocation]
level: advanced
status: docs-checked
description: "Private PKI on Certificate Authority Service: CA pools with root and subordinate CAs, DevOps vs Enterprise tiers, templates and issuance policies, revocation and CRLs."
sources: ["https://cloud.google.com/certificate-authority-service/docs/creating-ca-pool", "https://cloud.google.com/certificate-authority-service/docs/creating-certificate-authorities", "https://cloud.google.com/certificate-authority-service/docs/certificate-template", "https://cloud.google.com/certificate-authority-service/docs/revoking-certificates", "https://github.com/cert-manager/google-cas-issuer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate Authority Service private PKI

**Goal:** an internal CA hierarchy with a root kept apart from the issuing CAs, certificates issued
from policy-constrained pools, and a revocation path you have tested.

## 1. Hierarchy and tiers
- **Root CA** in its own **CA pool**, with subordinate (issuing) CAs in separate pools per purpose
  (`workload-mtls`, `internal-tls`, `device`). Keep the root disabled except when signing a subordinate.
- Tier per pool: **DevOps** vs **Enterprise**. The tier decides whether CA Service persists the certificates it
  creates, whether they can later be revoked, and the maximum rate at which certificates can be created. CAs in
  Enterprise tier pools can publish CRLs to the pool's Cloud Storage bucket. Pick Enterprise when you need revocation or a record of what was issued.
```bash
gcloud privateca pools create root-pool --location=europe-west1 --tier=ENTERPRISE
gcloud privateca roots create root-ca --pool=root-pool --location=europe-west1 \
  --key-algorithm=ec-p384-sha384 --subject="CN=Example Root CA, O=Example" --max-chain-length=2 --validity=P10Y
gcloud privateca pools create issuing-pool --location=europe-west1 --tier=ENTERPRISE \
  --issuance-policy=policy.yaml --publish-ca-cert --publish-crl
gcloud privateca subordinates create workload-ca --pool=issuing-pool --location=europe-west1 \
  --issuer-pool=root-pool --issuer-location=europe-west1 --subject="CN=Example Workload CA" --validity=P3Y
gcloud privateca roots disable root-ca --pool=root-pool --location=europe-west1
```
Choose CA key storage (CA Service key or your own Cloud KMS key) per the CA creation page; a Cloud KMS key keeps control of protection level, location and rotation, and the CA Service agent needs access to it: a disabled, destroyed or inaccessible key stops issuance and management operations.

## 2. Issuance policy (what a pool will sign)
The pool's issuance policy restricts what its CAs may issue: allowed key types, maximum lifetimes, SAN constraints and backdating options. Pass it as YAML or JSON with `--issuance-policy`; the CA pool page documents the exact schema, so build the file from there and not from memory.

**Certificate templates** (`gcloud privateca templates create`) are reusable profiles. A principal needs `roles/privateca.templateUser` to use one; grant it to the specific service accounts or groups that should mint that kind of certificate.

## 3. Issue
```bash
gcloud privateca certificates create api-cert --issuer-pool=issuing-pool --issuer-location=europe-west1 \
  --csr=api.csr --cert-output-file=api.pem --validity=P30D
```
`roles/privateca.caManager` (CA Service Operation Manager) manages CAs and templates. For automation on GKE, the `google-cas-issuer` project (cert-manager external issuer, `github.com/cert-manager/google-cas-issuer`) issues from a CA pool.

## 4. Revoke, rotate, retire
- CA Service revokes certificates by serial number or resource name with an optional reason (`--reason`). A revoked certificate's serial number and reason appear in all future CRLs.
- Rotate an issuing CA by creating a new subordinate in the same pool and disabling the old one (`desired_state` ENABLED or DISABLED); a CA pool is designed to make CA rotation easier.
- Distribute only the root as a trust anchor, not subordinates.

## Gotchas
- The tier choice is made at pool creation; decide it before issuing.
- Deleting or disabling the Cloud KMS key behind a CA breaks issuance and management for that CA.

## Verify
- [ ] `openssl verify -CAfile root.pem -untrusted sub.pem api.pem` passes.
- [ ] A certificate outside the pool's issuance policy is refused.
- [ ] A revoked certificate's serial appears in the published CRL.

## Checked
2026-10-28. Confirmed on the CA Service creating-ca-pool, creating-certificate-authorities, certificate-template and revoking-certificates pages: DevOps vs Enterprise tier effects, CRL publishing for Enterprise pools, issuance policy contents, `roles/privateca.templateUser`, `roles/privateca.caManager`, `ec-p384-sha384`, `--publish-crl`, `--reason`, ENABLED/DISABLED CA state, Cloud KMS key dependency. gcloud commands and flags passed check_commands. Removed: price remarks, 24 hour and validity guidance, issuance policy YAML example (field names not found on the fetched pages), certificate-manager issuance-config command (page not found), OCSP statement, deletion grace period, location and region claims, role list beyond the two confirmed, GKE and mesh specifics, bucket and trust-store notes.
Method: documentation only; no commands were run.
