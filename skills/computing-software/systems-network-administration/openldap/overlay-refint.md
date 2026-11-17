---
id: computing-software.systems-network-administration.openldap.overlay-refint
name: overlay-refint
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, refint, referential-integrity, overlay, refint-nothing]
level: practitioner
status: docs-checked
description: "Keep DN-valued attributes consistent after deletes and renames with the OpenLDAP refint overlay: refint_attributes, refint_nothing, modifiersname, rootdn need."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-refint&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# refint overlay
```
overlay refint
refint_attributes member manager
refint_nothing "cn=admin,dc=example,dc=com"
```
- `refint_attributes <attr> [...]`: attributes (must have distinguishedName syntax) to keep consistent.
- `refint_nothing <string>`: placeholder, which must be a valid DN, used when removing the last value would violate a required attribute (otherwise: Object Class Violation and the request fails).
- `refint_modifiersname <DN>`: modifiersName for overlay updates; default `cn=Referential Integrity Overlay`.

Behaviour: deleting `uid=robert,ou=people,dc=example,dc=com` removes that DN from every referencing attribute (e.g. `manager`). Renaming it to `uid=george,...` rewrites matching values to the new DN.

Gotchas:
- The database must have a `rootdn` (the overlay runs as it); no `rootpw` needed.
- Overlay changes are not replicated: configure it identically on every consumer.
- Directives must come after `overlay refint`.

Verify: delete a referenced entry, then `ldapsearch -x -b <base> '(manager=<deleted dn>)'` should return nothing.

## Checked
2026-11-08: confirmed against the slapo-refint(5) man page (all three directives, rootdn requirement, no replication of overlay changes, placement after overlay) and the Admin Guide overlays chapter section 12.11 (read that section only, not the whole chapter; distinguishedName syntax, refint_nothing behaviour).
Method: documentation only; no commands were run.
