---
id: computing-software.systems-network-administration.openldap.rwm-mapping-and-rewrite-rules
name: rwm-mapping-and-rewrite-rules
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, rewrite-rules, rwm-map, rewrite-contexts, rwm, rewriterule, attribute-mapping]
level: sme
status: docs-checked
description: "Write OpenLDAP rwm rewriteRule patterns with flags and contexts, and rwm-map attribute and objectClass mapping, including blank handling and email-to-DN bind."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-rwm&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rwm mapping and rewrite rules
Rule: `rwm-rewriteRule <regex> <substitution> [flags]` inside `rwm-rewriteContext <name>`. Use `$1..$9`, `$0`, `$$`; never `\`. Rules recurse by default.

Flags: `C` case-sensitive; `R` POSIX basic regex (default extended); `M{n}` max passes; `:` apply once; `@` stop after match; `#` stop with "unwilling to perform"; `G{n}` jump n rules; `I` ignore errors; `U{n}` return code. Order matters: `IG{2}` jumps on match and error, `G{2}I` only on match.

Contexts, client to server: `default`, `bindDN`, `searchDN`, `searchFilter`, `searchFilterAttrDN`, `compareDN`, `addDN`, `modifyDN`, `renameDN`, `newSuperiorDN`, `deleteDN`, `exopPasswdDN`; server to client: `searchEntryDN`, `searchAttrDN`, `matchedDN`, `referralDN`.

Examples:
```
rwm-rewriteContext addBlanks
rwm-rewriteRule "(.*),([^ ].*)" "$1, $2"
rwm-rewriteContext default
rwm-rewriteRule ".*" "${>addBlanks($0)}" ":"

rwm-rewriteMap ldap attr2dn "ldap://host/dc=my,dc=org?dn?sub"
rwm-rewriteMap escape dn2filter unescapedn escape2filter
rwm-rewriteContext bindDN
rwm-rewriteRule "^(mail=)([^,]+@[^,]+)$" "${attr2dn($1${dn2filter($2)})}" ":@I"

rwm-map objectclass groupOfNames groupOfUniqueNames
rwm-map attribute uniqueMember member
rwm-map attribute cn *
rwm-map attribute *
```
The last map line drops every attribute not explicitly mapped.

Gotchas: reaching the pass limit (`rwm-rewriteMaxPasses`) counts as success and recursion is simply interrupted; regex backslashes must be doubled (`\\.`); map URIs must name exactly one attribute (use `entryDN` for the DN). The overlay is marked experimental in the man page.

## Checked

2026-11-09. Confirmed against the slapo-rwm(5) man page (OpenLDAP 2.6): rwm-map semantics, rewriteRule syntax and flags (pattern matching and action), flag ordering example, substitution syntax and `$` escaping, context names, rewriteMap and the email bind example, max passes behaviour. The context lists in the skill are the main ones, not every name on the page (it also lists compareAttrDN, addAttrDN, modifyAttrDN, referralAttrDN and newRDN). Nothing was removed.
Method: documentation only; no commands were run.
