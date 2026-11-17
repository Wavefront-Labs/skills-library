---
id: computing-software.cybersecurity-defensive.endpoint-security.uac-hardening
name: uac-hardening
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [uac-hardening, user-account-control, admin-approval-mode, secure-desktop, uac-bypass, administrator-protection, windows-endpoint-protections]
level: practitioner
status: docs-checked
description: "Harden User Account Control: always notify on the secure desktop, credential prompts for standard users, admin approval mode for RID 500, and UAC's limits as a boundary."
sources: ["https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/settings-and-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UAC hardening

UAC splits an administrator's token so programs run unprivileged until elevation is approved. Microsoft
does **not** treat UAC as a security boundary (many public bypasses, UACME catalogues them) - the real
control is users not being local admins. Still, harden it.

## Recommended settings (Security Options)
| Setting | Value |
|---|---|
| Admin Approval Mode for the Built-in Administrator account | Enabled |
| Behaviour of the elevation prompt for administrators in Admin Approval Mode | Prompt for consent on the secure desktop - or "Prompt for credentials on the secure desktop" for stronger |
| Behaviour of the elevation prompt for standard users | Automatically deny elevation requests (users raise tickets/EPM) or prompt for credentials |
| Detect application installations and prompt for elevation | Enabled |
| Only elevate UIAccess apps installed in secure locations | Enabled |
| Run all administrators in Admin Approval Mode (EnableLUA) | Enabled - disabling turns UAC off entirely and breaks modern apps |
| Switch to the secure desktop when prompting | Enabled |
| Virtualize file and registry write failures | Enabled |

Registry values (`ConsentPromptBehaviorAdmin`
= 2 always notify on secure desktop, `ConsentPromptBehaviorUser` = 0 deny).

## Administrator protection
Newer Windows 11 feature; see Microsoft's Administrator protection documentation and evaluate it when available in your builds.

## Checked
2026-10-28. Confirmed in the UAC settings and configuration page: `ConsentPromptBehaviorAdmin` (2 = consent on the secure desktop) and `ConsentPromptBehaviorUser` (0 = automatically deny). Removed: the registry key path, the `LocalAccountTokenFilterPolicy` section, CIS level references (CIS pages are not readable) and the description of Administrator protection internals.
Method: documentation only; no commands were run.

## Verify
- [ ] `ConsentPromptBehaviorAdmin`, `EnableLUA` values compliant fleet-wide.
- [ ] Standard user elevation attempts denied (or routed to EPM).
