---
id: computing-software.messaging-and-integration.apache-camel.message-filter
name: message-filter
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, filter, predicate, statuspropertyname]
level: intro
status: docs-checked
description: "Camel Filter EIP: predicate scoped to child steps, statusPropertyName, and using Stop in the block to drop non-matching messages."
sources:
  - https://camel.apache.org/components/next/eips/filter-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message Filter

Works like `if (predicate) { block }`. Options: `expression` (required predicate), `statusPropertyName` (exchange property that stores the boolean result), `outputs` (child steps), `disabled` (default `false`, build-time only).

Scope: the filter applies only to its child steps.
- Predicate true: the message runs the child steps, then continues on the route.
- Predicate false: it skips the child steps and continues after the filter.
- To stop routing non-matching messages entirely, put a Stop EIP in the filter block.

Body is unchanged going into the child steps. The EIP defines no exchange properties; to record the outcome set `statusPropertyName`. With `statusPropertyName="gold"` the property `gold` holds true or false either way.

Predicate examples: Simple `${header.foo} == 'bar'`, XPath `/person[@name='James']`, or a bean method `isGoldCustomer` returning a boolean.

Verify: with `statusPropertyName` set, a non-matching message still reaches later steps and carries the property as false.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Filter EIP page source (filter-eip.adoc) and the Filter model definition (filter.json) from the apache/camel repository, which generate the cited page. Confirmed the if-block behaviour, scope limited to child steps, expression, statusPropertyName stored as a boolean, disabled default false and build-time only, the Stop EIP advice, and the Simple, XPath and bean examples. Nothing was removed. No commands were run.
