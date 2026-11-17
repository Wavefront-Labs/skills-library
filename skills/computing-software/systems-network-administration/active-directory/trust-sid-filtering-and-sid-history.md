---
id: computing-software.systems-network-administration.active-directory.trust-sid-filtering-and-sid-history
name: trust-sid-filtering-and-sid-history
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-trusts, sid-filtering, quarantine-trust, sid-history, enablesidhistory, netdom-quarantine, migration, privilege-escalation, treat-as-external]
level: advanced
status: gated
description: "Understand and control SID filtering on trusts: quarantine on external trusts, forest trust filtering, temporarily allowing SID history during migration, and the risks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-trust
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4675
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SID filtering and SID history across trusts

## Why it exists
A user's token includes SIDs from `sIDHistory`. Without filtering, an admin in the trusted
forest could write a privileged SID of *your* forest (e.g. your Domain Admins) into a user's
sIDHistory and gain that privilege across the trust. SID filtering drops SIDs in the
authorization data that do not belong to the trusted domain/forest.

## Defaults
The netdom reference lists `/quarantine` as `Yes` accepts only SIDs from the directly trusted domain, `No` accepts any SID (default). Typical behaviour by trust type, which no readable page confirms (gated: unconfirmed, source is paywalled or blocked): forest trusts filter SIDs that do not belong to the trusted forest; external trusts use quarantine; no filtering inside a forest.

## Inspect
```powershell
Get-ADTrust -Filter *
netdom trust ad.example.com /domain:fabrikam.example /quarantine
netdom trust ad.example.com /domain:fabrikam.example /enablesidhistory
```

## Migration: temporarily allow SID history
During an ADMT migration, migrated users carry their old SIDs in sIDHistory so they keep
access to old resources. For that to work across a **forest** trust the resource side must allow it:
```cmd
netdom trust ad.example.com /domain:fabrikam.example /enablesidhistory:yes /usero:... /passwordo:*
```
For an external trust: `/quarantine:no`. Re-enable filtering when the migration is finished
and resources are re-ACLed (`/enablesidhistory:no`, `/quarantine:yes`), then clear
sIDHistory from accounts.

## Risks and rules
- `/enablesidhistory:yes` is valid only for outbound forest trusts and should be enabled only if you trust the administrators of the trusted forest. Use it only for the migration window.
- Audit with event 4675 (SIDs were filtered) on DCs to see filtering in action.

## Verify
- [ ] After migration: `/quarantine` and `/enablesidhistory` report filtering back on; no users retain sIDHistory
  (query users that still have a `sIDHistory` value) (gated: unconfirmed, source is paywalled or blocked).

## Checked
Checked 2026-10-27 against Microsoft Learn (netdom trust reference; event 4675 reference).
- Confirmed: /quarantine yes accepts only SIDs from the directly trusted domain, default listed as No; /enablesidhistory valid only for outbound forest trusts with the trust-the-administrators warning; event 4675 is "SIDs were filtered".
- Gated: the per-trust-type default behaviour and the sIDHistory query. Reason: the SID filtering articles are protocol specifications or previous-versions pages that could not be read.
- Removed: the RID range claim and Get-ADTrust property names.

Method: documentation only; no commands were run.
