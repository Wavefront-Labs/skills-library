---
id: computing-software.systems-network-administration.openldap.overlay-memberof
name: overlay-memberof
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, memberof, reverse-group-membership, overlay, groupofnames]
level: practitioner
status: docs-checked
description: "Maintain memberOf attributes in OpenLDAP with the memberof overlay: defaults, memberof-group-oc, dangling handling, refint, addcheck and replication caveats."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-memberof&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# memberof overlay
```
overlay memberof
```
Defaults: `memberof-group-oc groupOfNames`, `memberof-member-ad member`, `memberof-memberof-ad memberOf`.

Other directives:
- `memberof-dn <DN>`: modifiersName for internal updates (default the database rootdn).
- `memberof-dangling ignore|drop|error` (default `ignore`); `memberof-dangling-error <code>` (default constraint violation).
- `memberof-refint TRUE|FALSE`: update groups when a member's DN changes.
- `memberof-addcheck TRUE|FALSE`: on Add, populate memberOf from groups already referencing the entry; works only with dangling `ignore`.
- cn=config: `olcMemberOfConfig` (the old `olcMemberOf` is deprecated).

Gotchas:
- Name `memberOf` in the attribute list, as the guide's example does: `ldapsearch ... "(uid=test1)" memberOf`.
- Set `memberof-group-oc` when you use a group class other than `groupOfNames`.
- Overlay changes are internal and not replicated; run memberof on each consumer and exclude the attribute from replication with `exattrs`.
- Subtree renames are not handled by memberof-refint; use the refint overlay.
- For less demanding environments, the dynlist overlay can provide the same functionality.

## Checked
2026-11-08: confirmed against the slapo-memberof(5) man page (every directive, default, the 2.5 olcMemberOfConfig rename, replication and exattrs note, subtree-rename note) and the Admin Guide overlays chapter section 12.8 (read that section only, not the whole chapter). Reworded the "operational" claim, which the pages do not state, and the dynlist remark.
Method: documentation only; no commands were run.
