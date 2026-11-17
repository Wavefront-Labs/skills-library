---
id: computing-software.messaging-and-integration.apache-camel.variables
name: variables
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, variables, exchange, state, scopes]
level: practitioner
status: docs-checked
description: "Camel 4.4+ variables: exchange, route, group and global scopes, Java and Simple access, application.properties initial values."
sources:
  - https://camel.apache.org/manual/variables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables (Camel 4.4+)

Four scopes:
- **Exchange** (default while routing): private to one Exchange.
- **Route**: `route:<routeId>:<name>`.
- **Group**: `group:<groupName>:<name>`.
- **Global**: `global:<name>`, shared across the CamelContext.

Headers received through `VariableReceive` are stored as `header:<variable>.<headerName>` and are read-only.

Java: `exchange.setVariable("myKey", value)`, `exchange.getVariable("myKey", String.class)`, `exchange.setVariable("global:myGlobalKey", value)`. `context.getVariable("name")` reads the global scope. A route variable set inside a route without an id implies the current route.

DSL: the `setVariable`, `removeVariable` and `convertVariableTo` EIPs. Simple reads `${variable.name}`; `variable("name")` works as an expression, e.g. in `setBody`.

Initial values in application.properties:
- `camel.variable.name = value` (global)
- `camel.variable.route.<routeId>.<name>`
- `camel.variable.group.<group>.<name>`
Values may use `resource:file:`, `resource:classpath:`, `#bean:`, `#class:` or `#valueAs(type):`.

Versus exchange properties: Camel uses properties internally; variables are reserved for users. Versus headers: variables are a separate store focused on the body, so you avoid juggling headers or Claim Check.

Verify: `setVariable` then `${variable.myKey}` in a later step returns the value even after the body changes.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel Variables manual page. Confirmed: available from Camel 4.4, exchange, route, group and global repositories, Java get and set with global:, route: and group: prefixes, context.getVariable reading global, implied current route, setVariable, removeVariable and convertVariableTo EIPs, Simple access, camel.variable.* initial values with route and group prefixes and the resource:, #bean:, #class: and #valueAs forms, header:<variable>.<header> read-only header variables, and the contrast with exchange properties and headers.
