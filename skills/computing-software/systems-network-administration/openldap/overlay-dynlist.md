---
id: computing-software.systems-network-administration.openldap.overlay-dynlist
name: overlay-dynlist
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, dynlist, dynamic-groups, dynlist-attrset, groupofurls, memberof]
level: advanced
status: docs-checked
description: "Build dynamic lists and dynamic groups in OpenLDAP with the dynlist overlay: dynlist-attrset syntax, member and memberOf expansion, dgIdentity and caveats."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-dynlist&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dynlist overlay
Syntax: `dynlist-attrset <group-oc> [URI] <URL-ad> [options]`. The `URL-ad` must be a subtype of `labeledURI`; `overlay dynlist` must come first. Include `dyngroup.schema` for `groupOfURLs`.

Examples:
```
overlay dynlist
dynlist-attrset groupOfURLs memberURL
```
Entry: `memberURL: ldap:///ou=People,dc=example,dc=com?mail?sub?(objectClass=person)` collects the mail addresses into the entry.

- Filterable list: `dynlist-attrset groupOfURLs memberURL mail:mail` (map `mapped-ad:list-ad`).
- Dynamic group: `dynlist-attrset groupOfURLs memberURL member` with a URI that has no attribute list: `ldap:///ou=People,dc=example,dc=com??sub?(objectClass=person)`.
- With memberOf: `dynlist-attrset groupOfURLs memberURL member+dgMemberOf`, or `member+memberOf@groupOfNames` to include static groups. A trailing `*` nests groups (Search only, not Compare).

Authorization: expansions run as the requester; `dgIdentity` (dyngroup schema) names another DN, a zero-length value makes it anonymous; `dgAuthz` limits who may use it.

Gotchas:
- `dynlist-simple TRUE` reverts to 2.4 behaviour and drops memberOf, nesting and filtering.
- For a dynamic group the URI must omit the attrs portion; the member attribute lists the DNs of the matching entries.
- The manageDSAit control disables expansion.
- cn=config names `olcDynListAttrSet`/`olcDynListConfig` replace deprecated `olcDlAttrSet`/`olcDynamicList`.

## Checked

2026-11-04. Confirmed against slapo-dynlist(5): dynlist-attrset syntax and options, URL-ad as a labeledURI subtype, mapped-ad:list-ad for lists, member-ad[+memberOf-ad[@static-oc[*]]] for groups, nesting only for Search, dynlist-simple behaviour, dgIdentity (zero-length string) and dgAuthz from the dyngroup schema, manageDSAit disabling expansion, and the renamed olcDynListAttrSet and olcDynListConfig. Removed the claim that it can replace slapo-memberof and the memberUid remark, which are not on the page.

Method: documentation only; no commands were run.
