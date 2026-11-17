---
id: computing-software.cloud-infrastructure-engineering.azure.application-gateway-mutual-tls-client-certificates
name: application-gateway-mutual-tls-client-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-gateway, mtls, ssl-profile, client-certificates, mutual-tls, rewrite-rules]
level: advanced
status: docs-checked
description: "Require client certificates at Application Gateway v2: trusted client CA chains, SSL profiles on listeners, DN and revocation checks, and passing cert details to backends."
sources: ["https://learn.microsoft.com/azure/application-gateway/mutual-authentication-overview", "https://learn.microsoft.com/azure/application-gateway/mutual-authentication-cli", "https://learn.microsoft.com/azure/application-gateway/rewrite-http-headers-url#mutual-authentication-server-variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application Gateway mutual TLS

**Goal:** only clients presenting a certificate from your CA (partners, devices, B2B APIs) reach the backend.

## 1. Trusted client CA certificate
Upload the CA chain (root plus intermediates) as a PEM or CER file; Microsoft recommends one chain per file. Each SSL profile
supports up to 100 trusted client CA chains and one gateway up to 200:
```bash
az network application-gateway client-cert add -g rg --gateway-name agw-prod -n partner-ca --data ./partner-ca-chain.cer
```

## 2. SSL profile with client authentication
```bash
az network application-gateway ssl-profile add -g rg --gateway-name agw-prod --name mtls-partners \
  --client-auth-configuration True --trusted-client-certificates partner-ca \
  --policy-type Predefined --policy-name <predefined-policy>
az network application-gateway http-listener update -g rg --gateway-name agw-prod -n lst-api-https --ssl-profile-id <ssl-profile-resource-id>
```
Modes: **strict** (a valid client certificate is required during the handshake) and **passthrough** (the gateway asks for a
certificate but continues without one, and the backend does the validation).
Options: verify the client certificate's immediate issuer DN (off by default), and revocation checking with OCSP
(`verifyClientRevocation: OCSP`, API 2022-05-01 or later; CRL is not supported; no portal support). The access log property
`sslClientVerify` shows the OCSP result. Keep the OCSP responder highly available and reachable from the gateway.

## 3. Pass identity to the backend
Rewrite rule adding request headers from server variables:
- `X-Client-Cert` = `{var_client_certificate}` (PEM, URL-encoded)
- `X-Client-Cert-Verify` = `{var_client_certificate_verification}` (strict mode: SUCCESS; passthrough mode: PASSTHROUGH or NONE)
- `X-Client-Cert-Subject` = `{var_client_certificate_subject}`; also `_issuer`, `_serial`, `_fingerprint` (SHA1), `_start_date`, `_end_date`.
The backend authorises on subject/fingerprint - AGW only proves the cert chains to the CA.
Strip any client-supplied headers with the same names to prevent spoofing.

## Gotchas
- Upload a chain that includes the intermediates; with issuer DN verification, uploading several chains in one file gives unexpected DN extraction.
- Rotate expiring CA certificates before client certificates stop validating.

## Verify
- [ ] `curl --cert client.pem --key client.key https://api.contoso.com` succeeds; in strict mode a request without a certificate is rejected; backend logs show the subject header.

## Checked
2026-10-28. Confirmed in Learn mutual-authentication-overview and the rewrite-http-headers-url server variable table: strict and
passthrough modes, 100/200 chain limits, PEM/CER upload, issuer DN option, OCSP revocation limits, sslClientVerify, variable
names and verification values. check_commands flagged `-n` on `ssl-profile add` (should be `--name`) and `--ssl-profile` on
`http-listener update` (the flag is `--ssl-profile-id`); both fixed. Removed: the FAILED:reason value, the per-listener and
TLS-error-versus-HTTP gotchas, the backend mTLS note, the exact SSL policy name. The mutual-authentication-cli page returned 404.
Method: documentation only; no commands were run.
