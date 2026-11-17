---
id: computing-software.cybersecurity-defensive.identity-access-management.certificate-based-authentication
name: certificate-based-authentication
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [certificate-based-authentication, cba, entra-cba, smart-card-logon, piv, x509-authentication, phishing-resistant-mfa]
level: advanced
status: docs-checked
description: "Deploy certificate-based authentication: Entra CBA and on-prem smart card logon, CA trust, user binding rules, strong mapping (KB5014754), CRL availability and rollout."
sources: ["https://learn.microsoft.com/en-us/entra/identity/authentication/concept-certificate-based-authentication", "https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-certificate-based-authentication", "https://support.microsoft.com/en-us/topic/kb5014754-certificate-based-authentication-changes-on-windows-domain-controllers-ad2c23b0-15d8-4340-a468-4d4f3b188f16"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate-based authentication

## Entra ID CBA
1. Upload the root/issuing CA certificates (PKI-based trust store in Entra), with CRL distribution point URLs reachable from the internet.
2. Authentication methods -> Certificate-based authentication: enable for a pilot group.
3. **Username binding**: map a certificate field to a user attribute. Prefer high-affinity bindings - SKI, SHA1PublicKey, or IssuerAndSerialNumber against `certificateUserIds` - over low-affinity (PrincipalName/RFC822Name to UPN), which trust whatever name the CA put in.
4. **Authentication binding**: set policy OIDs or issuers that count as multi-factor (smart card with PIN) vs single-factor (software cert).
5. Use as phishing-resistant MFA in Conditional Access authentication strengths.

## On-prem smart card logon (AD)
- Certificate template suitable for smart card logon, with the private key on a smart card, PIV key or TPM virtual smart card.
- DCs need valid domain controller certificates trusted by clients.
- KB5014754 strong certificate mapping: certificates must carry the SID security extension or be explicitly strongly mapped (`altSecurityIdentities`, for example X509SKI or X509SHA1PublicKey). Check the KB for the current enforcement phase; weak mappings fail in Full Enforcement mode.
- Consider requiring smart card for interactive logon on admin accounts.

## Gotchas
- An unreachable CRL distribution point can break CBA sign-ins; publish CRLs to highly available HTTP.
- Low-affinity binding plus a CA that issues certificates with attacker-chosen SANs = impersonation (ESC-style attacks). Lock down enrolment templates.
- Mobile clients need certificate delivery (Intune PKCS/SCEP or a YubiKey with NFC).

## Verify
- [ ] Pilot users sign in with CBA; sign-in log shows authentication method "X.509 Certificate" and MFA satisfied.
- [ ] Revoked test certificate is rejected.
- [ ] No weak-mapping audit events remain on DCs.

## Checked

2026-10-28. Confirmed against the Entra CBA concept and how-to pages and the KB5014754 article: certificateUserIds bindings, high-affinity SKI, SHA1PublicKey and IssuerAndSerialNumber vs low-affinity PrincipalName and RFC822Name, X509SKI and X509SHA1PublicKey strong altSecurityIdentities mappings, authentication binding for multifactor vs single-factor. Removed: szOID extension name, 'Full Enforcement is now default' (check the KB for the current phase), smart-card-required hash rotation claim, NTAuth and EKU specifics, DC event ids 39/40/41.

Method: documentation only; no commands were run.
