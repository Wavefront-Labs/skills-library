---
id: computing-software.data-engineering.apache-nifi.expression-language-boolean-functions
name: expression-language-boolean-functions
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, expression-language, boolean, routing, routeonattribute]
level: practitioner
status: docs-checked
description: "NiFi Expression Language boolean functions for routing rules: isNull, equals, matches, find, contains, in, comparisons, not and ifElse, with exact examples."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boolean functions

- Null/empty: `${filename:isNull()}`, `${filename:notNull()}`, `${filename:isEmpty()}`
- Equality: `${filename:equals('hello.txt')}`, `${filename:equalsIgnoreCase('hello.txt')}`
- Regex: `${filename:matches('a.*txt')}` (whole value), `${filename:find('brand')}` (anywhere)
- Substring: `${filename:contains('new')}`
- Membership: `${myEnum:in("PAUL", "JOHN", "MIKE")}`
- Comparison: `${filename:length():ge(5)}` (also `gt`, `lt`, `le`)
- Negate: `${filename:equals('hello.txt'):not()}`
- Choose: `${bool:ifElse('a','b')}`
- Combine with `and`/`or` taking sub-expressions.

Semantics from the guide: `matches` needs the whole subject to match the Java regex, `find` matches any sequence inside it; `gt`/`ge`/`lt`/`le` return false if subject or argument cannot be coerced to a Number; `and`/`or` return false if an operand cannot be coerced to a Boolean; `isEmpty` is also true for whitespace-only values; `ifElse` returns a String.

Verify: evaluate each expression against a test FlowFile and compare with the guide's examples.

## Checked

Confirmed against the Expression Language guide (Boolean Logic functions, contains/in/find/matches). Removed the RouteOnAttribute relationship and unmatched claims, which are processor behaviour not covered by the cited page.

Method: docs-only read of cited pages, 2026-11-08
