---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workload-identity-federation-with-x509-certificates
name: workload-identity-federation-with-x509-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, wif-x509, x509-federation, mtls, trust-store, on-premises-workloads, keyless-auth]
level: practitioner
status: docs-checked
description: "Let on-prem or other-cloud workloads with X.509 client certificates obtain Google credentials via mTLS Workload Identity Federation: trust store, attribute mapping, cred config."
sources: ["https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates", "https://cloud.google.com/sdk/gcloud/reference/iam/workload-identity-pools/providers/create-x509"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload Identity Federation with X.509 certificates

For workloads that already have a PKI identity (SPIFFE, internal CA, device certs) but no OIDC/SAML
issuer. The workload presents its client certificate over mTLS to the STS endpoint.

## Trust store
```yaml
# trust_store.yaml: PEMs inline
trustStore:
  trustAnchors:
  - pemCertificate: "-----BEGIN CERTIFICATE-----\n...root...\n-----END CERTIFICATE-----"
  intermediateCas:
  - pemCertificate: "-----BEGIN CERTIFICATE-----\n...issuing...\n-----END CERTIFICATE-----"
```

## Provider
```bash
gcloud iam workload-identity-pools create onprem --location=global
gcloud iam workload-identity-pools providers create-x509 corp-pki \
  --location=global --workload-identity-pool=onprem \
  --trust-store-config-path=trust_store.yaml \
  --attribute-mapping="google.subject=assertion.subject.dn.cn" \
  --attribute-condition="assertion.san.uri=='spiffe://example/path'"
```
The default subject is the certificate subject common name (`assertion.subject.dn.cn`); `assertion.san.uri` can match a SPIFFE ID, as the guide's condition example shows.

## Credential configuration
```bash
gcloud iam workload-identity-pools create-cred-config \
  projects/<PN>/locations/global/workloadIdentityPools/onprem/providers/corp-pki \
  --service-account=batch@<P>.iam.gserviceaccount.com \
  --credential-cert-path=/etc/pki/client.pem --credential-cert-private-key-path=/etc/pki/client.key \
  --credential-cert-trust-chain-path=/etc/pki/chain.pem \
  --output-file=cred.json
export GOOGLE_APPLICATION_CREDENTIALS=$PWD/cred.json
```
`create-cred-config` also produces a certificate configuration file (`--credential-cert-configuration-output-file` sets its path); client libraries use it for mTLS to the Security Token Service
(the guide also covers regional `*.rep.mtls.googleapis.com` endpoints).

## Gotchas
- Client certificates must chain up to one of the trust anchors in the trust store; add intermediate CAs under `intermediateCas`.
- Certificate rotation is your PKI's job; the cred config points to file paths, rotate in place.
- Anyone with a certificate from that CA matching the condition gets in: keep conditions tight.

## Verify
- [ ] `gcloud auth login --cred-file=cred.json && gcloud storage ls gs://<B>` works from the host.
- [ ] A cert from another OU is denied.

## Checked

- Date: 2026-10-27
- Confirmed against the WIF with X.509 certificates guide (trust store YAML with `trustStore`, `trustAnchors`, intermediate CAs; default `google.subject=assertion.subject.dn.cn`; `assertion.san.uri` SPIFFE condition; chaining to trust anchors; certificate config for mTLS) and the gcloud references for `providers create-x509` (`--trust-store-config-path`, `--attribute-mapping`, `--attribute-condition`) and `create-cred-config` (`--credential-cert-path`, `--credential-cert-private-key-path`, `--credential-cert-trust-chain-path`, `--credential-cert-configuration-output-file`).
- Removed: the OU mapping and condition example (not in the guide), `sts.mtls.googleapis.com` as the fixed endpoint, library-version and `invalid_grant` claims.

Method: documentation only; no commands were run.
