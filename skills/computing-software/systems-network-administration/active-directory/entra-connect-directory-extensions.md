---
id: computing-software.systems-network-administration.active-directory.entra-connect-directory-extensions
name: entra-connect-directory-extensions
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, directory-extensions, attribute-filtering, azure-ad-connect, schema-extensions]
level: advanced
status: docs-checked
description: "Sync custom or extra on-premises AD attributes to Entra ID with Entra Connect directory extensions and attribute filtering, and read them in Graph."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-feature-directory-extensions
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-configure-filtering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect directory extensions and attribute filtering

## Directory extensions
Extend the Entra schema with attributes from on-premises AD that are not in the default sync set (including custom schema
attributes). Currently no Microsoft 365 workload consumes them, but dynamic group rules and Graph can.

1. Entra Connect wizard > **Customize synchronization options** > Optional features > tick
   **Directory extension attribute sync**.
2. On the **Directory Extensions** page pick attributes. Valid candidates: User and Group object types; single-valued
   String, Boolean, Integer and Binary; multi-valued String and Binary.
3. Finish. The wizard registers the attributes on the **Tenant Schema Extension App** (a system-only app that cannot be
   deleted).

In Entra they appear as `extension_<appIdWithoutDashes>_<attributeName>` and can be read through Microsoft Graph.

## Attribute filtering
The optional feature **Microsoft Entra app and attribute filtering** adds wizard pages that let you tailor which
attributes are synchronized. Note that Connect Health will not upload sync-error events when attribute filtering has
been changed from the default.

## Gotchas
- An object can have up to 100 directory extension attribute values; each value of a multi-valued attribute counts. String
  values are truncated at 256 characters.
- Not supported: constructed attributes (for example `msDS-UserPasswordExpiryTimeComputed`) and non-replicated attributes
  (`badPwdCount`, `lastLogon`, `lastLogoff`).
- Not all Entra features support multi-valued extension attributes; check the feature you plan to use.
- The attribute list is read from the AD schema at install. After extending the AD schema, run the wizard task to refresh
  the directory schema before new attributes appear.
- Manage directory extensions only through the wizard. Manually editing or cloning their sync rules is not supported.
- Importing exported settings creates the rule but does not map the attributes: re-select them on the new server.
  Selected attributes are not carried by the settings export, so reapply them after a swing migration.
- Do not sync into extension attributes that Connect did not create.

## Verify
- [ ] A test user's extension property appears in Graph after a delta cycle
  (`Start-ADSyncSyncCycle -PolicyType Delta`).

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect directory extensions page, the custom installation page,
the import and export configuration page and Connect Health sync monitoring. Confirmed object types, attribute types, the
100-value limit, 256-character truncation, unsupported attribute kinds and the swing-migration caveat. Corrected: the
limit is per object (not per tenant), devices are not listed as extension objects, and the wizard page is named
"Microsoft Entra app and attribute filtering". Removed the Graph PowerShell snippet and the stale-value claim.
Method: documentation only; no commands were run.
