---
id: computing-software.systems-network-administration.active-directory.cloud-sync-attribute-mapping-expressions
name: cloud-sync-attribute-mapping-expressions
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, cloud-sync-attribute-mapping, expressions, provisioning, on-demand-provisioning]
level: advanced
status: docs-checked
description: "Customize Entra Cloud Sync attribute mappings: direct, constant and expression mappings, functions like Join and Switch, and testing with provision on demand."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-attribute-mapping
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/reference-expressions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Sync attribute mapping and expressions

Cloud Sync uses the same provisioning engine as Entra app provisioning, so mappings are edited in the Entra admin
center per configuration: Cloud sync > the configuration > **Attribute mapping**.

## Mapping types
- **Direct**: source AD attribute to target Entra attribute.
- **Constant**: fixed value (for example `usageLocation` = `AU`).
- **Expression**: a script-like expression over source attributes (Expression Builder and the expression reference).
- **None**: the target is left alone, but if it is ever empty it is filled with the default value you set.
- Apply this mapping: **Always** (create and update) or **Only during creation**.
- Default value if null: provisioned only when the object is created, not on updates.

## Expression syntax
Expressions are built only from functions, `FunctionName(arg, ...)`, which can nest. Arguments are attributes in square
brackets (`[sn]`), string constants in double quotes, or other functions. A backslash or quote inside a string is escaped
with a backslash.

Signatures from the function reference:
- `IIF(condition, valueIfTrue, valueIfFalse)`
- `Switch(source, defaultValue, key1, value1, key2, value2, ...)` (keys and values in pairs; the default can be `""`)
- `Replace(source, oldValue, regexPattern, regexGroupName, replacementValue, replacementAttributeName, template)`;
  leave unused arguments empty

```text
Join(" ", [givenName], [sn])
Switch([c], "", "AU", "Australia", "GB", "United Kingdom")
IIF(IsNullOrEmpty([mail]), Join("@", [sAMAccountName], "example.com"), [mail])
Replace([userPrincipalName], "@ad.example.local", , , "@example.com", , )
ToLower([sAMAccountName])
```
Test an expression in the Expression Builder before saving.

## Test
1. Configuration > **Provision on demand**, enter a user distinguished name, select **Provision**.
2. Read the step output for scoping, matching and the attribute values computed.
3. Check the provisioning logs for skips or errors.

## Gotchas
- Changing a mapping affects objects on later cycles; restart sync to apply it to everything sooner.
- Do not change the matching attribute on a live configuration without a plan: the wrong match creates duplicates.

## Verify
- [ ] Provision on demand shows the expected computed values and Success.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Cloud Sync attribute mapping page and the expression
reference. Confirmed mapping types, the Always and Only during creation options, default-value behaviour, the
`IIF`, `Switch` and `Replace` signatures and the provision-on-demand steps. Corrected the `Switch` example, which was
malformed. Removed the unsourced claims about case-sensitive function names and the default matching attribute.
Method: documentation only; no commands were run.
