---
id: computing-software.search-and-information-retrieval.apache-solr.copyfield-catchall
name: copyfield-catchall
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [copy-fields, copy-field, catchall-field, copyfield, maxchars, default-search-field]
level: practitioner
status: docs-checked
description: "Copy Solr fields with copyField to analyze one value several ways or build a catchall default search field, including maxChars, wildcards, and the no-chaining rule."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/copy-fields.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# copyfield-catchall

`<copyField source="cat" dest="text" maxChars="30000"/>` copies the source before analysis, so the destination can use a different analysis chain and storage from the original.

Details:
- If the destination already has its own values, the copied values are added as extra values.
- Mark the destination `multiValued="true"` when it receives several values (several sources or a multivalued source).
- `maxChars` caps the characters copied per value and so controls index growth. Copy fields do grow the index.
- Source and dest can use a leading or trailing `*`. A wildcard in `dest` requires a wildcard in `source`; the matching glob portion names the destination.
- Copying happens at the stream level and copies do not chain: copying a to b and b to c does not put a into c. The same source may go to many destinations.

Common use: copy title, author, keywords and body into one catchall field, then make it the default query field in `solrconfig.xml`.

For atomic updates, copy destinations must be `stored="false"`.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Copying Fields page: copy before analysis, extra values on the destination, `multiValued`, `maxChars`, index growth, leading or trailing wildcards and the dest wildcard rule, no chaining, one source to many destinations, and the catchall default query field. The atomic update `stored="false"` rule is from the Partial Document Updates page. Nothing removed.

Method: documentation only; no commands were run.
