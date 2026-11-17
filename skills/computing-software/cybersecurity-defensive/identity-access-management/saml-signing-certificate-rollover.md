---
id: computing-software.cybersecurity-defensive.identity-access-management.saml-signing-certificate-rollover
name: saml-signing-certificate-rollover
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sso, saml-certificate-rollover, saml, token-signing-certificate, federation-metadata, entra-id, adfs, okta, saml-certificate-rollover-metadata, saml-certificate-rollover-metadata]
level: practitioner
status: draft
description: "Roll SAML token-signing certificates without breaking SSO: inventory apps, metadata-URL vs manual apps, overlap periods, Entra/AD FS/Okta steps, and expiry monitoring."
sources: ["https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/tutorial-manage-certificates-for-federated-single-sign-on", "https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/ad-fs-certificates-overview", "https://help.okta.com/en-us/content/topics/apps/manage-signing-certificates.htm"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SAML signing certificate rollover

Every SAML app trusts the IdP's signing certificate. When it expires or rotates, apps that pinned the
old certificate reject logins. Rollovers are routine; outages come from not knowing which apps pin.

## Inventory
- Entra: Enterprise applications > each SAML app > Single sign-on > SAML Certificates (expiry, status).
  Graph: `GET /servicePrincipals?$filter=preferredSingleSignOnMode eq 'saml'` with `keyCredentials`.
- AD FS: `Get-AdfsCertificate -CertificateType Token-Signing`; relying party trusts list.
- Okta: per app Sign On tab > SAML Signing Certificates.
For each app record: does the SP consume IdP metadata from a URL (auto-updates) or was the
certificate uploaded manually?

## Entra procedure (per app)
1. Create a new certificate (SAML Certificates > Edit > New Certificate), set expiry (up to 3 years).
2. Give the app owner the new certificate or metadata. Many SPs accept two IdP certificates: add the
   new one alongside the old.
3. Make the new certificate Active at the agreed time; test login.
4. Remove the old one from the SP after confirming.
Entra emails notification addresses 60, 30 and 7 days before expiry; set a monitored distribution list.

## AD FS
AutoCertificateRollover (default on) creates a secondary token-signing cert 20 days before expiry and
promotes it 5 days before. RPs reading federation metadata update automatically; manual RPs need the
secondary cert added during that window. Check: `Get-AdfsProperties | fl AutoCert*,CertificateGenerationThreshold,CertificatePromotionThreshold`.

## Emergency rotation (suspected key compromise)
Token-signing key theft (Golden SAML) lets attackers forge assertions for any user. Rotate twice (as
with krbtgt) so the stolen key is no longer trusted, update all SPs, and investigate. Prefer moving off
AD FS to cloud IdP where the key is not on servers you must defend.

## Monitoring
- Scheduled report of certificates expiring in 60 days across IdPs.
- Alert on certificate changes on SAML apps (audit logs: "Update application - Certificates and secrets management").

## Gotchas
- SPs that cache metadata for days; time the switch accordingly.
- Some SPs validate the certificate chain/expiry strictly; self-signed IdP certs are normal in SAML
  and expiry is what matters.
- Encryption certificates (SP side) are a separate rollover.

## Verify
After activation: successful test login per app, SAML tracer shows the new certificate thumbprint in
the signature, and sign-in logs show no SAML signature errors (AADSTS errors at SP side).
