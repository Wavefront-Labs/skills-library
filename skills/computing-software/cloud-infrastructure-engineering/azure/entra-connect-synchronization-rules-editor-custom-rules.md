---
id: computing-software.cloud-infrastructure-engineering.azure.entra-connect-synchronization-rules-editor-custom-rules
name: entra-connect-synchronization-rules-editor-custom-rules
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-connect, sync-rules-editor, sync-rule-precedence, inbound-sync-rule, attribute-flow, hybrid-identity]
level: advanced
status: docs-checked
description: "Write custom Entra Connect sync rules safely: precedence, scoping, expressions, cloning defaults, preview, and full sync after changes."
sources: ["https://learn.microsoft.com/entra/identity/hybrid/connect/how-to-connect-create-custom-sync-rule", "https://learn.microsoft.com/entra/identity/hybrid/connect/concept-azure-ad-connect-sync-declarative-provisioning", "https://learn.microsoft.com/entra/identity/hybrid/connect/how-to-connect-sync-change-the-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect custom sync rules

**Goal:** change what syncs and how attributes map without editing (and losing) the out-of-box rules.

## Rules of the road
- Changes to the default out-of-box rules are overwritten the next time Entra Connect is updated. Default rules carry a thumbprint, so edits also cause problems applying later releases. Make changes only as described below.
- **Precedence**: a lower number wins a conflict (highest precedence = lowest numeric value). Out-of-box rules start at 100 and 1-99 is reserved for custom rules. Pick a value no other rule uses. Leave the Tag box empty: only Microsoft's out-of-box rules have a tag.
- To customise a default rule, clone it with Edit: the copy is made and the original disabled. Save the clone with precedence below 100. Ideally keep only the attribute you change in the clone and re-enable the default rule, so the rest still comes from the default.
- If your clone computes NULL for an attribute and the default rule gives a value, the non-NULL value wins. Use `AuthoritativeNull` as the source (FlowType Expression) to stop lower-precedence rules contributing.
- Only one sync rule with join rules may be in scope for an object, otherwise an error occurs; precedence does not resolve join conflicts.
- More than 99 custom rules: Microsoft documents a PowerShell method using `PrecedenceBefore` set to the out-of-box rule's Identifier with Precedence 0 (do not set ImmutableTag); the new rule gets 100 and the out-of-box rules shift up.

## Procedure (Microsoft's given-name example)
```powershell
Set-ADSyncScheduler -SyncCycleEnabled $false   # scheduler runs every 30 minutes by default
```
1. Synchronization Rules Editor > Inbound > Add new rule.
2. Connected system: Active Directory connector; object types User and Person; Link Type Join; unique precedence (Microsoft's other example uses 50).
3. Scoping filter, for example `givenName ISNOTNULL`. An empty filter applies to all user objects, including conference rooms and service accounts.
4. Leave Join rules empty to let the out-of-box rule handle joins.
5. Transformations: FlowType Expression, Target `givenName`, Source `PCase([givenName])`.
6. Function and attribute names are case-sensitive; a typo shows a warning when you add the rule, and you must reopen and correct it.
7. Verify in Synchronization Service: either Run > Full Synchronization on the connector, or Search Connector Space, pick an object, Preview, then Commit Preview. Check the object in Metaverse Search, including the Sync Rules column.
8. Re-enable:
```powershell
Set-ADSyncScheduler -SyncCycleEnabled $true
```

## Moving rules between servers
In the rules editor, Export on a selected rule produces a PowerShell script that re-creates it, which is how to move a rule from one server to another.

## Gotchas
- String attributes are indexable with a maximum length of 448 characters. For longer values Microsoft's flow trims with `Left(Trim(Item([description],1)),448)` inside an `IIF(IsNullOrEmpty(...),NULL,...)`.
- A full synchronization recalculates all objects with the current rules.
- Press F5 in the editor to reset filtering and load a fresh configuration.

## Verify
- [ ] Preview or metaverse search shows the expected value and the new rule in the Sync Rules column.
- [ ] Scheduler re-enabled.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages how-to-connect-sync-change-the-configuration, how-to-connect-create-custom-sync-rule and concept-azure-ad-connect-sync-declarative-provisioning (keyword and section reads). Removed unconfirmed: `cloudFiltered` filtering and its delete behaviour, `Start-ADSyncSyncCycle -PolicyType Initial`, `New-ADSyncRule`, the export deletion threshold and its cmdlet, csexport, the staging server advice, sourceAnchor warning and the Get-MgUser check.
