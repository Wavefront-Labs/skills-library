---
id: computing-software.systems-network-administration.openldap.ldapsearch-options
name: ldapsearch-options
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ldapsearch, search-filter, search-scope, ldif-output, extensions]
level: practitioner
status: docs-checked
description: "Use ldapsearch effectively: connection and auth flags, base and scope, filters, attribute selection (*, +, 1.1), LDIF output, paging, sorting and extensions."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldapsearch&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldapsearch options
Pattern: `ldapsearch [opts] [filter] [attrs...]`. Default filter `(objectClass=*)`; default scope `sub`.

Auth/connection: `-x` simple; `-D binddn` with `-W` (prompt), `-w pw` or `-y file`; `-H uri`; `-Z`/`-ZZ` StartTLS; SASL: `-Y mech -U authcid -R realm -X authzid -O props -I/-Q -N`; `-M[M]` manageDSAit.

Search: `-b base`; `-s base|one|sub|children`; `-a never|always|search|find`; `-l` time limit and `-z` size limit (0 or `none` unlimited, `max`); `-S attr` sort client-side (buffers all results); `-f file` one search per line with `%s` substitution (`-c` to continue).

Attributes: none or `*` all user attributes; `+` operational; `1.1` none (DNs only).

Output: `-L` LDIFv1 only, `-LL` no comments, `-LLL` no version line; `-A` names only; `-u` user-friendly DN; `-t`/`-tt` temp files for values; `-o ldif_wrap=<width>|no`; `-v`, `-n`.

Extensions (`-E`): `pr=<size>[/prompt|noprompt]` paged results; `sss=[-]<attr[:OID]>` server-side sort; `vlv=<before>/<after>(/<offset>/<count>|:<value>)`; `sync=ro|rp[/cookie]`; `deref=...`; `subentries`; `mv=<filter>`. General (`-e`): `assert`, `postread`, `preread`, `relax`, `ppolicy`, `noop`.

Examples:
```
ldapsearch -LLL "(sn=smith)" cn sn telephoneNumber
ldapsearch -LLL -s one -b "c=US" "(o=University*)" o description
ldapsearch -x -b dc=example,dc=com -E pr=100/noprompt '(objectClass=person)' 1.1
```
Exit status 0 on success; non-zero prints a diagnostic to stderr.

## Checked

2026-11-09. Confirmed against ldapsearch(1) for 2.6: default filter and scope, attribute selectors (*, +, 1.1), -L levels, -S client-side sort, -z and -l limits, -f pattern with %s and -c, -a values, -t and -tt, -u, -A, -o ldif_wrap, SASL flags, the -e general and -E search extension lists, and the three examples.

Method: documentation only; no commands were run.

