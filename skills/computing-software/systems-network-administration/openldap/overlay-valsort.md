---
id: computing-software.systems-network-administration.openldap.overlay-valsort
name: overlay-valsort
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, valsort, value-sorting, weighted, overlay, valsort-attr]
level: practitioner
status: docs-checked
description: "Sort multi-valued attributes in OpenLDAP search results with valsort-attr: alpha and numeric modes, weighted values with {n} prefixes, and the valsort control."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-valsort&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# valsort overlay
Syntax after `overlay valsort`:
`valsort-attr <attribute> <baseDN> (<sort-method> | weighted [<sort-method>])`

Methods: `alpha-ascend`, `alpha-descend`, `numeric-ascend`, `numeric-descend`, `weighted`.

```
overlay valsort
valsort-attr member ou=groups,dc=example,dc=com alpha-ascend
valsort-attr memberUid ou=Groups,dc=example,dc=com weighted
```
Weighted mode: prefix values with an integer weight, e.g. `memberUid: {4}admin`, `memberUid: {2}dovecot`. Weighted always sorts ascending; an optional second method orders equal weights. The `{n}` prefix is stripped from results unless the client sends the valsort control.

See the weights with the control (OID 1.3.6.1.4.1.4203.666.5.14, BER boolean TRUE):
`ldapsearch -E 1.3.6.1.4.1.4203.666.5.14=::MAMBAf8= ...`

Gotchas:
- Sorting happens whenever the attribute is returned in a search response.
- Alphanumeric methods are invalid on Integer or NumericString syntax attributes; numeric methods are invalid on anything else.
- `valsort-attr` must follow the `overlay` line.

## Checked

2026-11-04. Confirmed against slapo-valsort(5) and the Administrator's Guide overlays chapter: valsort-attr syntax, four sort methods and weighted with optional secondary method, errors for method versus syntax, sorting on search response, {n} weight prefix stripped unless the control 1.3.6.1.4.1.4203.666.5.14 is sent with {b} value, the base64 ldapsearch -E example, the member and memberUid examples with weights 4, 2.

Method: documentation only; no commands were run.
