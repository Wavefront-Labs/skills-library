---
id: computing-software.cybersecurity-defensive.identity-access-management.machine-identity
name: machine-identity
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [machine-identity, non-human-identities, workload-identity, certificate-inventory, secrets-sprawl, service-principals, spiffe]
level: advanced
status: draft
description: "Manage machine and non-human identities: inventory of service accounts, keys, certificates and tokens, ownership, short-lived credentials, rotation and anomaly monitoring."
sources: ["https://owasp.org/www-project-non-human-identities-top-10/", "https://spiffe.io/docs/latest/spiffe-about/overview/", "https://csrc.nist.gov/pubs/sp/1800/16/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Machine identity management

Non-human identities (service accounts, service principals, API keys, OAuth apps, SSH keys, TLS
certificates, CI tokens) outnumber humans many times over and rarely have MFA or owners.

## Programme
1. **Discover:** AD service accounts (`servicePrincipalName` set, password never expires), Entra service principals and app credentials, AWS IAM users with access keys and roles, GCP service account keys, Kubernetes service accounts, CI/CD secrets, certificates (CT logs + internal scanners), secrets in code (secret scanning).
2. **Own:** each identity has a human owner and an application; unowned = disable candidate.
3. **Prefer short-lived, keyless credentials:** managed identities, IAM roles, workload identity federation (OIDC from GitHub Actions/Kubernetes to clouds), SPIFFE/SPIRE SVIDs, gMSA for Windows services.
4. **Rotate what remains:** secrets in a vault with automated rotation; certificates via ACME/automated CLM (lifetimes trending to 47 days for public TLS by 2029).
5. **Least privilege:** scope per workload, no shared identities across apps or environments.
6. **Monitor:** usage from new IPs/ASNs, credential added to an existing service principal (classic persistence), unused identities for 90 days.

## OWASP NHI Top 10 (2025) themes
Improper offboarding, secret leakage, vulnerable third-party NHIs, insecure authentication, overprivileged
NHIs, insecure cloud deployment configs, long-lived secrets, environment isolation, NHI reuse, human use of NHI.

## Gotchas
- Humans logging in as service accounts; deny interactive logon and alert.
- Rotating a secret without knowing all consumers causes outages; find consumers via logs first.

## Verify
- [ ] Inventory with owners covers each platform.
- [ ] Count of long-lived keys trending down; none older than policy.
