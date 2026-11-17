---
id: computing-software.cybersecurity-defensive.security-architecture.legacy-app-zero-trust
name: legacy-app-zero-trust
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [legacy-app-zero-trust, zero-trust, identity-aware-proxy, kerberos-constrained-delegation, application-proxy, ztna, header-based-authentication]
level: advanced
status: draft
description: "Bring legacy apps (Kerberos/NTLM, header auth, thick clients) under zero trust with identity-aware proxies, KCD, app connectors and microsegmentation compensating controls."
sources: ["https://learn.microsoft.com/en-us/entra/identity/app-proxy/overview-what-is-app-proxy", "https://learn.microsoft.com/en-us/entra/identity/app-proxy/how-to-configure-sso-with-kcd", "https://cloud.google.com/iap/docs/concepts-overview", "https://csrc.nist.gov/pubs/sp/800/207/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Legacy applications in a zero trust architecture

Legacy apps cannot speak OIDC/SAML or evaluate device posture. Put a policy enforcement point (PEP)
in front of them and translate.

## Patterns by app type
| App auth | Pattern |
|---|---|
| Windows Integrated Auth (Kerberos/NTLM) web app | Entra Application Proxy (or F5 APM, Akamai EAA) with **Kerberos Constrained Delegation**: user does modern auth + CA at the proxy, connector obtains a Kerberos ticket on their behalf |
| Header-based (SiteMinder style `REMOTE_USER`) | Proxy injects signed headers after OIDC login; app accepts headers only from the proxy's IP |
| Forms login | Password-vaulting SSO in the proxy, or replace the login with a reverse proxy enforcing auth before the form |
| Thick client / non-HTTP (RDP, SSH, SQL, SAP GUI) | ZTNA client-based app segments (per-port, per-host), or a PAM gateway |
| Cannot be changed at all | Microsegment it: only the PEP / jump host may reach it; log every flow |

## KCD with Entra App Proxy (outline)
1. Install the private network connector on a domain-joined server that can reach the app.
2. On the connector's computer object: Delegation -> trust for specified services only -> use any
   authentication protocol -> add the app's SPN (e.g. `HTTP/app01.corp.example.com`).
3. Enterprise app -> Single sign-on -> Windows Integrated Authentication, set the internal SPN and the
   delegated login identity (UPN or on-prem SAM name).
4. Apply Conditional Access (compliant device + MFA) to the enterprise app.

## Gotchas
- The app must reject direct access; otherwise users and attackers bypass the PEP. Firewall it to the connector only.
- Header injection is only safe if the app cannot be reached except via the proxy and the proxy strips client-supplied copies of the header.
- Protocol transition (any authentication protocol) is powerful; scope the SPN list tightly and monitor the connector host as tier 0-adjacent.
- Apps with hard-coded hostnames or absolute URLs need link translation or a split-DNS same-name publish.

## Verify
- [ ] Direct connection to the app from a user subnet fails.
- [ ] Access via the proxy from an unmanaged device is blocked by policy.
- [ ] Sign-in logs show the CA decision for each access.
