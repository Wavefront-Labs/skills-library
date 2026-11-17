---
id: computing-software.cybersecurity-defensive.endpoint-security.code-integrity-event-analysis
name: code-integrity-event-analysis
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [application-control, code-integrity-events, wdac, event-3076, event-3077, devicecontrol-events, audit-mode, policy-tuning]
level: advanced
status: draft
description: "Read App Control (WDAC) CodeIntegrity events to tune policies: 3076/3077 audit vs block, 3089 signature details, script events 8028/8029, and turning audit logs into rules."
sources: ["https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/operations/event-id-explanations", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/operations/querying-application-control-events-centrally-using-advanced-hunting", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/audit-appcontrol-policies"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CodeIntegrity event analysis

## Where
Event Viewer > Applications and Services Logs > Microsoft > Windows > CodeIntegrity > Operational,
and AppLocker > MSI and Script for script enforcement. Centrally: Defender advanced hunting
`DeviceEvents` with `ActionType` starting `AppControl`.

## Key event IDs
| ID | Meaning |
|---|---|
| 3076 | Audit: file would have been blocked (audit-mode policy) |
| 3077 | Enforced: file blocked |
| 3089 | Signature information for a 3076/3077 (correlated by correlation ID); publisher, issuer, hashes |
| 3033/3034 | Image did not meet signing level (e.g. not WHQL / Microsoft-signed) |
| 3099 | Policy loaded (name, ID, options): proves which policies are active |
| 8028/8029 | Script/MSI audit/block (AppLocker MSI and Script log) |
| 8036 | COM object blocked |

## Advanced hunting
```kql
DeviceEvents
| where ActionType in ("AppControlCodeIntegrityPolicyAudited","AppControlCodeIntegrityPolicyBlocked")
| extend p = parse_json(AdditionalFields)
| summarize devices=dcount(DeviceName), count() by ActionType, FileName, FolderPath,
            Publisher=tostring(p.PublisherName), PolicyName=tostring(p.PolicyName)
| order by devices desc
```

## From audit to rules
1. Run the policy in audit mode for 2-4 weeks across representative devices.
2. Group 3076 events by publisher/product. Prefer allowing by **publisher + product name** (signer
   level), then by file path only for admin-writable locations, hashes only for unsigned stragglers.
3. Generate rules from events: App Control Policy Wizard "Policy Editor > parse event logs", or
   `New-CIPolicy -Audit -Level Publisher -Fallback Hash -UserPEs` on a reference machine, then merge
   (`Merge-CIPolicy`) into a supplemental policy.
4. Redeploy, confirm 3076 volume falls to known unsigned junk, then switch to enforced.

## Triage of blocks in production
- 3077 + 3089: identify signer; is this a legitimate new app version (update the supplemental policy)
  or malware/unwanted (good block)?
- Driver blocks (3033 with kernel files) after hardware updates: vendor-signed driver missing WHQL;
  check the vendor.

## Gotchas
- Managed installer and ISG-allowed files do not generate events when allowed; blocks come from
  files outside those paths.
- Event logs roll over quickly on busy machines; collect centrally.
- Multiple policies: a file must be allowed by every base policy; 3099 shows which are active.

## Verify
After each policy update, a test unsigned binary is blocked (3077) and top business apps show no 3076/3077
events for a week.
