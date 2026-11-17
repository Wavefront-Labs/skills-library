---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-patch-idp-quirks
name: scim-patch-idp-quirks
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-patch-idp-quirks, scim-patch, interoperability, entra-id, patch-quirks, tolerant-reader, boolean-strings, identity-protocols]
level: advanced
status: docs-checked
description: "Cope with Entra ID SCIM PATCH differences from RFC 7644: capitalised op, string booleans, path-less replace; build a tolerant server."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2
  - https://learn.microsoft.com/en-us/entra/identity/app-provisioning/application-provisioning-config-problem-scim-compatibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PATCH interoperability quirks across IdPs

Goal: make your SCIM server work with real provisioning clients.

RFC 7644 section 3.5.2: the PATCH body carries `schemas` with `urn:ietf:params:scim:api:messages:2.0:PatchOp` and an `Operations` array; each operation has exactly one `op` that MAY be `add`, `remove` or `replace`. SCIM PATCH does not support array indexing or JSON Patch operations such as `move`.

Microsoft Entra provisioning (Learn page "Known issues and resolutions with SCIM 2.0 protocol compliance") documents that without its compliance flag the sync engine sends:
- `"op": "Replace"`, `"Add"` and `"Remove"` with a capital first letter.
- Disabling a user as `replace` on `active` with the string value `"False"`; with the flag it sends `"replace"` and the boolean `false`.
- Replacing several attributes as separate operations; with the flag it combines them into one path-less `replace` whose `value` is an object of attribute names, alongside filtered paths such as `emails[type eq "work"].value`.
- Removing a group member as `remove` on `members` with a `value` array; with the flag it sends `members[value eq "<id>"]` as the path.
The flag is the value `aadOptscim062020` added to the tenant URL; the page lists the "Update PATCH behavior to ensure compliance" item as not yet fixed by default, and says the flag does not currently work with on-demand provisioning. Entra's rollback value is `AzureAdScimPatch2017`. Re-read the page before relying on any of this: it is a moving target.

Method: capture real requests from the IdP's provisioning logs and implement a tolerant reader: normalise `op` case, accept boolean and string `active`, and accept both path-less object values and filtered paths. Keep strict RFC output when you write responses.

Gotchas:
- Group membership removal can arrive either as a `members` array or as a filtered path; handle both.
- The flag is set in the IdP, not on your server; tell tenant admins which behaviour you expect.

Verify: run the IdP's provisioning test against your endpoint and compare the logged request bodies with the shapes above.

## Checked

2026-11-09. Read RFC 7644 section 3.5.2 intro and the Microsoft Learn Entra SCIM compatibility page in full (flags section with sample requests). Removed: Okta claims, the probing-filter GET behaviour, "Entra stops on filter errors", "empty bodies break some clients" and the "historically" wording; none appear in the pages.
Method: documentation only; no commands were run.
