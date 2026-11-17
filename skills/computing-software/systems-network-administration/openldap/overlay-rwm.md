---
id: computing-software.systems-network-administration.openldap.overlay-rwm
name: overlay-rwm
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, rwm, suffixmassage, rewrite-engine, overlay, relay]
level: advanced
status: docs-checked
description: "Use the OpenLDAP rwm rewrite/remap overlay for DN suffix massaging with rwm-suffixmassage and rwm-rewriteEngine, and know its directive set and defaults."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-rwm&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/backends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rwm overlay
Experimental. Usually stacked on the `ldap`/`meta` proxy backends or the `relay` backend (which requires it).

Directives:
- `rwm-rewriteEngine {on|off}`: off disables rewriting without removing config.
- `rwm-suffixmassage [<virtual naming context>] <real naming context>`: shortcut that sets the engine on and generates rules:
```
rwm-suffixmassage "dc=virtual,dc=example" "dc=example,dc=com"
```
Without a virtual context it must appear after the `suffix` directive. It does not rewrite `searchFilter`, `referralAttrDN` or `referralDN` by default.
- `rwm-rewriteContext`, `rwm-rewriteRule`, `rwm-rewriteMap`, `rwm-rewriteParam`, `rwm-rewriteMaxPasses <passes> [<per rule>]` (default safe value 100): see the rewrite-rules skill.
- `rwm-map {attribute|objectclass} [<local>|*] {<foreign>|*}`: schema mapping.
- `rwm-normalize-mapped-attrs {yes|no}` (default no).
- `rwm-drop-unrequested-attrs {yes|no}` (default yes).

Generated suffix-massage rules mirror: `default` context rewrites virtual to real; `searchEntryDN` rewrites real to virtual; `searchAttrDN` and `matchedDN` alias `searchEntryDN`.

Gotchas:
- Rewriting the empty or subschema DN breaks root DSE and schema reads; overlays instantiated before a database can touch the empty DN.
- `nameAndOptionalUID` values are not rewritten.
- Unnormalized mapped values can mislead pcache; consider `rwm-normalize-mapped-attrs yes`.

## Checked

2026-11-04. Confirmed against slapo-rwm(5) and the Administrator's Guide backends chapter: experimental status, use with ldap, meta and relay backends (back-relay requires rwm), rwm-rewriteEngine, rwm-suffixmassage form and its automatic engine on, no searchFilter or referral rewriting by default, rwm-rewriteMaxPasses default 100, rwm-map syntax, rwm-normalize-mapped-attrs default no, rwm-drop-unrequested-attrs default yes, generated default, searchEntryDN, searchAttrDN and matchedDN contexts, the empty and subschema DN warning, nameAndOptionalUID not rewritten, pcache normalization note.

Method: documentation only; no commands were run.
