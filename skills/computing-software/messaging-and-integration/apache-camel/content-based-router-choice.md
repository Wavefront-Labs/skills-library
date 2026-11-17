---
id: computing-software.messaging-and-integration.apache-camel.content-based-router-choice
name: content-based-router-choice
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, choice, content-based-router, precondition]
level: intro
status: docs-checked
description: "Camel Choice EIP (content-based router): when and otherwise, first-match rule, endChoice in the Java DSL and precondition mode."
sources:
  - https://camel.apache.org/components/next/eips/choice-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choice (content-based router)

Options: `when` (list of predicates evaluated in order), `otherwise` (runs when nothing matches), `precondition` (default `false`), `disabled` (default `false`, build-time only).

"The first when clause that matches determines which route branch to follow." Each branch starts with the body the choice received; the EIP output is the body the executed branch ends with, or the original body if no branch ran. There are no exchange properties.

Example: with Simple, `header.foo == 'bar'` goes to `direct:b`, `'cheese'` to `direct:c`, otherwise `direct:d`.

Java DSL: some EIPs (Load Balancer, Split) have their own sub-routes, and a plain `.end()` cannot return to the Choice scope. Use `.endChoice()`. If it still fails, split the route and link the parts with `direct:`.

Precondition mode selects one branch at startup and always runs it, so predicates cannot depend on message content. Use property placeholders (optional ones like `{{?foo}}` work), JVM system properties or environment variables. `otherwise` is optional; with no match no branch is chosen. It pairs well with route templates, whose parameters can drive the predicates.

For a decision table of literal values use the Switch EIP.

Verify: a message with `foo=cheese` reaches `direct:c` only.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Choice EIP page source (choice-eip.adoc) and the Choice model definition (choice.json) from the apache/camel repository, which generate the cited page. Confirmed the when and otherwise options, the first-match quotation, precondition default false and its startup behaviour with property placeholders, system properties and environment variables, optional placeholders, the endChoice explanation and the direct: fallback, route template pairing, the Switch tip, and the body flow. Nothing was removed. No commands were run.
