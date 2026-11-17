---
id: computing-software.cybersecurity-defensive.identity-access-management.banned-passwords-and-breach-checks
name: banned-passwords-and-breach-checks
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [password-policy, banned-password-list, breached-password-detection, have-i-been-pwned, k-anonymity, entra-password-protection, leaked-credentials]
level: practitioner
status: gated
description: "Block common and breached passwords at set and change time (Entra Password Protection, HIBP k-anonymity API) and detect accounts whose current passwords leaked."
sources: ["https://learn.microsoft.com/en-us/entra/identity/authentication/concept-password-ban-bad", "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-password-ban-bad-on-premises", "https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Banned passwords and breach checks

**Goal:** users cannot choose passwords attackers will guess first, and you know when a
current password appears in a breach.

## At password set/change
**Microsoft Entra Password Protection**
- Global banned list (Microsoft-maintained) plus a custom list (up to 1,000 terms: company,
  products, locations, sports teams). Matching is fuzzy: normalisation (leet speak, case) and substring scoring.
- On-prem AD: install the proxy service and DC agent on all DCs; start in audit mode, review
  the event logs, then switch to enforced mode (see the on-premises deployment article).

**Applications you build**: check candidate passwords against Pwned Passwords using
k-anonymity (only the first 5 hex characters of the SHA-1 leave your server) (gated: unconfirmed, source is paywalled or blocked):
```python
import hashlib, requests
h = hashlib.sha1(pw.encode()).hexdigest().upper()
r = requests.get(f"https://api.pwnedpasswords.com/range/{h[:5]}", headers={"Add-Padding": "true"}, timeout=5)
breached = any(line.split(":")[0] == h[5:] for line in r.text.splitlines())
```
Or download the full hash list and query locally (no external dependency).

## Detecting leaked current passwords
- **Entra ID Protection "Leaked credentials"** risk detection flags
  users whose credentials were found in breach dumps; pair with risk-based policies to force a secure change.
- On-prem: periodic audit comparing NT hashes against the HIBP NTLM list with a password-audit
  tool such as DSInternals (run on a protected host, results are sensitive).

## Response to a hit
Force password change at next sign-in, revoke sessions, check sign-in logs for use from
unusual locations, and ensure MFA is registered.

## Gotchas
- Blocklists only apply on change: existing weak passwords stay until reset or audit.
- Running hash audits requires replicating hashes (DCSync rights): do it from a Tier 0 host, delete outputs afterwards.
- Overlong custom lists of single common words block too much; target organisation-specific terms.

## Verify
- [ ] Test change to `CompanyName2026!` fails on-prem and in cloud.
- [ ] Leaked-credential detections route to an automated or SOC response.

## Checked

2026-10-28. Confirmed against the Entra Password Protection concept pages: custom banned list limited to 1,000 terms, fuzzy matching and substring matching, Leaked credentials detection in ID Protection. Gated: the Pwned Passwords k-anonymity snippet (no HIBP page fetched). Removed: DCAgent event log name, audit/enforce wording specifics, password hash sync requirement, DSInternals parameter name.

Method: documentation only; no commands were run.
