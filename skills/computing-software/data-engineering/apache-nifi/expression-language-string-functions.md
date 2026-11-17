---
id: computing-software.data-engineering.apache-nifi.expression-language-string-functions
name: expression-language-string-functions
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, expression-language, string-functions, updateattribute, regex]
level: practitioner
status: docs-checked
description: "NiFi Expression Language string functions with page examples: toUpper, toLower, trim, substring, substringBefore, replace, replaceAll, append and prepend."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/nifi-in-depth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String functions

- Case/space: `${filename:toUpper()}`, `${filename:toLower()}`, `${attr:trim()}`
- Slicing: `${filename:substring(0,1)}`, `${filename:substringBefore('.')}`
- Replace: `${filename:replace('.', '_')}` (literal), `${filename:replaceAll('\..*', '')}` (regex)
- Concatenate: `${filename:append('.gz')}`, `${filename:prepend('a brand new ')}`

Guide results for `filename` = "a brand new filename.txt": `substring(0,1)` gives "a"; `substringBefore('.')` gives "a brand new filename"; `replace('.', '_')` gives "a brand new filename_txt"; `replaceAll('\..*', '')` gives "a brand new filename"; `append('.gz')` gives "a brand new filename.txt.gz". `trim()` on " 1 2 3 " gives "1 2 3".

NiFi In Depth shows UpdateAttribute rewriting the `filename` attribute of a FlowFile.

Verify: the resulting attribute value shows correctly in the FlowFile attribute view.

## Checked

Confirmed against the Expression Language guide (String Manipulation functions and their example tables).

Method: docs-only read of cited pages, 2026-11-08
