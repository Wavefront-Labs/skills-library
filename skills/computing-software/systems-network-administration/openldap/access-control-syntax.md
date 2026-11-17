---
id: computing-software.systems-network-administration.openldap.access-control-syntax
name: access-control-syntax
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, access-control, what-selector, access-levels, acl, olcaccess]
level: practitioner
status: docs-checked
description: "Write OpenLDAP access directives: the to-what selectors (dn, filter, attrs, entry, children), by-who clauses, access levels and privilege letters."
sources:
  - https://www.openldap.org/doc/admin26/access-control.html
  - https://www.openldap.org/software/man.cgi?query=slapd.access&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# access control syntax
Form: `access to <what> by <who> <access> <control>` with one or more `by` clauses. Default policy is read for all.

What selectors:
- `*` everything; `dn.exact|regex|base|one|subtree|children=<dn>`; `filter=<RFC 4515>`; `attrs=<list>`; `attrs=<attr> val.<style>=<regex>`.
- `children` excludes the named entry, `subtree` includes it.
- Pseudo-attributes: `entry` (read/search an entry) and `children` (add/delete/rename). Adding or deleting needs write on the entry's `entry` and the parent's `children`; renaming needs write on both parents' `children`.

Access levels (each includes lower ones): none `=0`, disclose `=d`, auth `=dx`, compare `=cdx`, search `=scdx`, read `=rscdx`, write `=wrscdx`, manage `=mwrscdx`. Explicit privileges use `=`, `+`, `-` with letters `m w r s c x d 0`. Prefix `self` limits to the entry's own user (`selfwrite`).

Example:
```
access to attrs=userPassword
    by self write
    by anonymous auth
    by * none
access to *
    by self write
    by users read
```
Tips: use `dn.regex` explicitly (plain `dn=` is exact), anchor regexes with `^` and `$`, and never list the rootdn (it bypasses ACLs). Test with slapacl.

## Checked

2026-11-04. Confirmed against the Administrator's Guide Access Control chapter (8.2 and 8.4.9): the access directive grammar including self, priv {=|+|-}{m|w|r|s|c|x|d|0}+ and controls, what selectors and scope styles with the worked match example, filter and attrs forms, entry and children pseudo-attributes and the add, delete and rename rules, access level table with privilege letters, each level implying lower ones, default read policy, rootdn bypass, dn.regex versus plain dn=, anchoring regexes, selfwrite, slapacl pointer.

Method: documentation only; no commands were run.
