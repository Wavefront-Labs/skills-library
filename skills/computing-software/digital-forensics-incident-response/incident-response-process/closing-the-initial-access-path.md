---
id: computing-software.digital-forensics-incident-response.incident-response-process.closing-the-initial-access-path
name: closing-the-initial-access-path
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [vulnerability-remediation, eradication, initial-access, patching, cisa-kev, dfir]
level: practitioner
status: draft
description: "Close the exploited vulnerability and initial access path: patching, mitigations, compromise checks on edge devices, and proving the door is shut."
sources: ["https://www.cisa.gov/known-exploited-vulnerabilities-catalog", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/40/r4/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Closing the initial access path

**Goal:** the route the attacker used is no longer available, and equivalent routes are
checked too, before systems return to production.

## By vector
| Vector | Close it |
|---|---|
| Exploited edge device (VPN, firewall, Citrix, Exchange) | Patch per vendor advisory; run the vendor integrity/compromise checker; **assume credentials and session cookies on the device are stolen** (rotate local accounts, LDAP bind creds, certificates); factory reset/re-image if advised |
| Exposed RDP/SSH | Remove from internet; require VPN with MFA; review firewall for other exposures (Shodan/Censys your own ranges) |
| Phishing/credential theft | MFA everywhere (phishing-resistant for admins), conditional access, block legacy auth |
| Valid account from infostealer | Reset, re-enrol MFA, check the user's other accounts and devices |
| Web application flaw | Fix code, WAF virtual patch until deployed, review for web shells |
| Third-party/MSP | Restrict their access paths, require MFA, time-bound access |

## Patching under incident pressure
- Patching does not remove an existing compromise; investigate the device first.
- Check CISA KEV for every internet-facing product version you run, not only the exploited one.
- If no patch exists: vendor mitigation, disable feature, or take offline.

## Verify
- External scan from the internet confirms the port/service is closed or patched version
  responds.
- Attempt the original technique in a controlled way (e.g. login without MFA) and confirm it fails.
- Record the evidence of closure in the case; insurers and regulators ask for it.
