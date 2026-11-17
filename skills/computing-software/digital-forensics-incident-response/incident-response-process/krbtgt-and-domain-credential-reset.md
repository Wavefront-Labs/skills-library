---
id: computing-software.digital-forensics-incident-response.incident-response-process.krbtgt-and-domain-credential-reset
name: krbtgt-and-domain-credential-reset
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [krbtgt-reset, ad-credential-reset, golden-ticket, active-directory, eradication, dfir]
level: advanced
status: docs-checked
description: "Reset the KRBTGT password twice, wait out the ticket lifetime between resets, and rotate other domain credentials after Active Directory compromise."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-reset-the-krbtgt-password", "https://github.com/microsoftarchive/New-KrbtgtKeys.ps1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KRBTGT and domain credential reset

**Goal:** invalidate forged Kerberos tickets (golden tickets) and any credentials the
attacker harvested with domain admin or DCSync access.

## Why twice
Microsoft's forest recovery guide says to perform the krbtgt reset twice. The password
history value for the krbtgt account is 2 (the two most recent passwords), so resetting
twice clears the old passwords from the history and no other DC can replicate with this DC
using an old password.

## How long to wait
Wait 10 hours between the two resets. Ten hours is the default for the Maximum lifetime for
user ticket and Maximum lifetime for service ticket policy settings. If those settings were
changed, the minimum wait must be greater than the configured value. Deciding to shorten the
gap in an active compromise is a deliberate risk decision for the incident lead, not a
documented procedure.

## Procedure
1. Check Active Directory replication is healthy before starting.
2. Reset the krbtgt password on a writeable DC. The Microsoft procedure is: in Active
   Directory Users and Computers choose View > Advanced Features, open the domain's Users
   container, right-click the krbtgt account and select Reset Password. The password you
   type is not significant because the system generates a strong password automatically.
3. Let the change replicate to all DCs, wait the interval above, then repeat the reset.
4. The Microsoft procedure covers writeable DCs, not RODCs. RODC krbtgt accounts are named
   krbtgt_number; they are a separate case to plan for if an RODC is in scope.
5. A customised password filter (such as passfilt.dll) on a DC can make the reset fail with
   an error; Microsoft points to Knowledge Base article 2549833 for a workaround.

## Script option
`New-KrbtgtKeys.ps1` (Microsoft's archive repository) is described as resetting the krbtgt
password and related keys while minimising the likelihood of Kerberos authentication
issues. The repository is archived and read-only, and its readme says the script errors on
retired DCs that are offline but not removed from AD; remove those with metadata cleanup
first, or use a maintained fork and review it before use.

## Other credentials to rotate
Treat anything the attacker could read with domain admin rights as exposed: tier-0 admin
accounts, service accounts, trust and machine secrets. Remove attacker-created accounts,
malicious GPOs and rogue domain controllers as part of the same eradication work. The
cited pages do not enumerate these, so build the list from the incident scoping.

## Verify
Confirm from each DC that the krbtgt password last-set time reflects both resets, and that
users and services authenticate normally afterwards.

## Checked
Dated 2026-11-08. Confirmed against the Microsoft Learn page "Active Directory Forest
Recovery - Reset the krbtgt password": two resets, 10 hour wait and its tie to the ticket
lifetime settings, password history of 2, krbtgt_number naming for RODCs, GUI steps,
passfilt.dll note. Confirmed against the New-KrbtgtKeys.ps1 repository page: purpose,
archived status, offline-DC limitation. Removed as not stated by the pages: the repadmin
commands, the Set-ADAccountPassword one-liner, simulation-mode claim, event 4769, the
AZUREADSSOACC, LAPS, SIDHistory and AdminSDHolder items.
Method: docs-only read of cited pages, 2026-11-08
