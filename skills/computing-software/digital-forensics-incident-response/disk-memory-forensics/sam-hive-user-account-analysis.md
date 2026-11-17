---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.sam-hive-user-account-analysis
name: sam-hive-user-account-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [sam-hive, windows-registry, user-accounts, registry-explorer, regripper, dfir]
level: practitioner
status: draft
description: "Analyse the SAM hive for local user accounts: RIDs, creation, last logon, password change, logon counts, account flags and group membership with Registry Explorer and RegRipper."
sources: ["https://ericzimmerman.github.io/", "https://github.com/keydet89/RegRipper3.0", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SAM hive user account analysis

**Goal:** list local accounts and their activity metadata to spot attacker-created or
abused local accounts. Hive: `Windows\System32\config\SAM` (plus `.LOG1/.LOG2`).

## Where the data lives
`SAM\Domains\Account\Users\<RID hex>` with values:
- **F** (binary): last logon time, password last set, account expires, last failed logon
  (FILETIMEs), RID, account flags (ACB: disabled, password not required, normal account),
  failed logon count, logon count.
- **V** (binary): username, full name, comment, LM/NT hash data (encrypted with the boot key
  from SYSTEM).
`SAM\Domains\Account\Users\Names\<username>`: key **last write time** approximates account
creation; the key's default value type equals the RID.
`SAM\Domains\Builtin\Aliases\00000220` (Administrators, RID 544) `C` value lists member SIDs.

## Tools
```text
RECmd / Registry Explorer: SAM plugin shows a parsed user table (bookmarks: Users)
rip.pl -r SAM -p samparse          (RegRipper 3)
```
Always load the hive with transaction logs replayed (Registry Explorer prompts; RECmd
`--nl false` handling) or recent changes may be missing.

## What to look for
- Accounts with RIDs above the normal range created during the incident window (Names key
  last write time).
- Built-in Administrator (RID 500) or Guest (501) enabled unexpectedly.
- Password-not-required flag, recent password resets of local admin, logon counts jumping.
- Accounts added to Administrators or Remote Desktop Users aliases.

## Gotchas
- Domain accounts are not in SAM; for domain users use NTUSER/profile list and DC logs.
- Last logon in SAM updates only for local interactive/network logons using local accounts.
- On domain controllers, SAM holds only the DSRM account.

## Verify
Cross-check suspicious account creation with Security events 4720/4732 and the
`ProfileList` key in SOFTWARE (profile creation for the SID).
