---
id: computing-software.cybersecurity-defensive.security-architecture.vendor-integration-security-review
name: vendor-integration-security-review
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-design-review, vendor-integration-review, third-party-integration, saas-integration, oauth-scopes, data-flows, vendor-risk]
level: practitioner
status: draft
description: "Review the security of a third-party integration before go-live: data flows, authentication and scopes, network paths, vendor posture, logging and exit plan."
sources: ["https://www.cisa.gov/resources-tools/resources/secure-by-design", "https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final", "https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Third-party integration security review

**Goal:** before connecting a vendor product or SaaS to your systems (SSO, APIs, data feeds,
agents, embedded scripts), know what it can access, how it authenticates, and how to cut it off.

## 1. Describe the integration
Draw the data flow: which systems, which data (classification), direction, frequency,
protocol, where data is stored and processed (regions, sub-processors). Identify the
business owner and the technical owner.

## 2. Authentication and authorisation
- Inbound to you (vendor calls your APIs): per-vendor credentials, OAuth client credentials or
  mTLS, IP allowlisting as an extra layer, least-privilege scopes, rate limits.
- Outbound (you grant the vendor access to your SaaS/cloud): OAuth app consent with minimum
  scopes (`Mail.Read` for one mailbox is not `Mail.ReadWrite` for all), Entra application
  access policies to scope mailbox access; AWS cross-account roles with ExternalId and
  narrow policies rather than access keys.
- SSO for vendor admin consoles; SCIM provisioning; MFA enforced.
- No shared admin accounts handed to the vendor.

## 3. Network and execution
- Agents or appliances installed on your network: what they reach, update mechanism (signed?),
  who controls them remotely. Vendor remote support paths go through your PAM.
- Third-party JavaScript on your websites: subresource integrity, CSP, or self-hosting.
- Webhooks: verify signatures, restrict source.

## 4. Vendor posture
SOC 2 Type II / ISO 27001 reports (read exceptions and complementary user entity controls),
pen test summary, vulnerability disclosure policy, breach notification terms, data deletion
on termination, sub-processor list. Scale the depth to the data sensitivity.

## 5. Monitoring and exit
- Log the integration's actions (API calls, sign-ins of the service principal) to the SIEM
  with alerts on unusual volume or new scopes.
- Credential rotation schedule and owner.
- Kill switch: documented steps to revoke tokens/keys and disable the app quickly; data
  return/deletion on contract end.

## Output
Short review record: risks, required conditions (scopes reduced, MFA, logging), accepted
residual risks with approver, review date.

## Gotchas
- Integrations approved for a pilot and expanded silently; re-review on scope change.
- Vendor "needs Global Admin to install": almost never true long-term; use a scoped role after setup.
- Forgotten integrations after a vendor is dropped keep their tokens; tie to contract lifecycle.

## Verify
Check the live configuration matches the review conditions (granted scopes, network rules,
logging) and the kill switch works in a test.
