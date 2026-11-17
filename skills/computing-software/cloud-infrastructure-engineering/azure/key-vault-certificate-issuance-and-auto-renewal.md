---
id: computing-software.cloud-infrastructure-engineering.azure.key-vault-certificate-issuance-and-auto-renewal
name: key-vault-certificate-issuance-and-auto-renewal
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, key-vault, kv-certificates, certificate-auto-renewal, certificate-issuer, digicert, globalsign, certificate-policy, csr-merge]
level: practitioner
status: docs-checked
description: "Issue and auto-renew certificates in Key Vault: integrated CAs (DigiCert/GlobalSign), CSR merge for other CAs, lifetime actions, and consumers picking up new versions."
sources: ["https://learn.microsoft.com/azure/key-vault/certificates/about-certificates", "https://learn.microsoft.com/azure/key-vault/certificates/how-to-integrate-certificate-authority", "https://learn.microsoft.com/azure/key-vault/certificates/create-certificate-signing-request", "https://learn.microsoft.com/azure/key-vault/certificates/overview-renew-certificate", "https://learn.microsoft.com/cli/azure/keyvault/certificate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key Vault certificate issuance and auto-renewal

**Goal:** TLS certificates are issued into Key Vault, renew themselves before expiry, and every
consumer (App Gateway, App Service, Front Door, AKS) picks up the new version without a ticket.

## Certificate policy is the control point
```bash
az keyvault certificate get-default-policy > policy.json   # edit
```
The policy holds the issuer (`Self`, `Unknown`, or a configured issuer name), subject and SANs, validity in months, key
properties (key type, key length, exportable, reuse key on renewal) and lifetime actions. Supported key types are RSA,
RSA-HSM, EC, EC-HSM and oct; exportable keys are allowed only with RSA and EC, and HSM keys are non-exportable. A
lifetime action is a trigger (days before expiration or lifetime percentage) plus an action (`emailContacts` or
`autoRenew`). Certificate contacts are shared by all certificates in the vault.

## Path A - integrated CA (DigiCert, GlobalSign)
```bash
az keyvault certificate issuer create --vault-name kv-tls --issuer-name digicert \
  --provider-name DigiCert --account-id <acct> --password <api-key> --organization-id <org-id>
# policy.json: "issuerParameters": {"name": "digicert", "certificateType": "OV-SSL"}
az keyvault certificate create --vault-name kv-tls -n www-contoso-com -p @policy.json
az keyvault certificate pending show --vault-name kv-tls -n www-contoso-com
```
Key Vault handles end-to-end lifecycle for certificates from these two partner CAs (OV-SSL and EV-SSL validation types);
a renewal creates a new secret version with a new Key Vault identifier. Key Vault also auto-renews self-signed
certificates. Domain validation must stay valid at the CA.

## Path B - any other CA (CSR merge)
```bash
# issuerParameters.name = "Unknown"
az keyvault certificate create --vault-name kv-tls -n api-contoso-com -p @policy.json
az keyvault certificate pending show --vault-name kv-tls -n api-contoso-com --query csr -o tsv > api.csr   # wrap in BEGIN/END CERTIFICATE REQUEST
# submit CSR to CA, receive cert chain
az keyvault certificate pending merge --vault-name kv-tls -n api-contoso-com --file signed-chain.pem
```
With issuer `Unknown`, Key Vault does not enroll or renew the certificate: renewal is manual (an email-only policy
sends a notification when it is time to renew), so you repeat create-new-version and merge. You can automate this
by reacting to Event Grid near-expiry events with a Function that calls the CA's API.

## Consumers picking up renewals
Reference the **versionless** secret ID (`https://kv-tls.vault.azure.net/secrets/www-contoso-com`) so renewals flow
through. Each consumer has its own refresh interval; read its documentation and test a renewal rather than assuming a
figure. The Key Vault VM extension polls per `pollingIntervalInS` (see the VM extension skill).

## Gotchas
- A certificate is addressable as certificate, key and secret objects. Consumers needing the PFX/PEM with private key
  read the **secret** (role *Key Vault Secrets User*); the policy must mark the key exportable or the private key is not
  part of the secret value.
- Changing SANs requires a new policy and a new version.

## Verify
- [ ] `az keyvault certificate show --vault-name kv-tls -n <name> --query "{exp:attributes.expires, policy:policy.lifetimeActions}"`.
- [ ] Consumers serve the new thumbprint after a renewal test (`openssl s_client -connect host:443 | openssl x509 -noout -dates -fingerprint`).

## Checked
2026-10-27. Confirmed against Learn "About Key Vault certificates", "Integrate a CA", "Create a CSR/merge", "Renew
certificates" and the az keyvault certificate CLI reference (issuer create flags, pending show/merge, get-default-policy).
Removed: the per-consumer refresh table (App Gateway 4 h, App Service 24 h, Front Door 72 h, CSI 2 min and its flag;
none in fetched pages), the Let's Encrypt/acmebot note, "RSA 2048/3072" key sizes, and "exportable false cannot be used
by App Gateway/App Service". The `--query` property paths in Verify were not checked against a schema.
Method: documentation only; no commands were run.
