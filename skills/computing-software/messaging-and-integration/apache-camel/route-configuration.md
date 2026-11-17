---
id: computing-software.messaging-and-integration.apache-camel.route-configuration
name: route-configuration
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, route-configuration, error-handler, intercept, reuse]
level: practitioner
status: docs-checked
description: "Camel route configuration (3.12+): shared error handler, onException, onCompletion and intercept via routeConfigurationId matching."
sources:
  - https://camel.apache.org/manual/route-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route configuration

Available since Camel 3.12. It holds shared settings: Error Handler, OnException, OnCompletion and Intercept, so they need not be copied per route or made global.

Define (Java): extend `RouteConfigurationBuilder` and write the `configuration()` method (not `configure()`):
- `routeConfiguration("id")` for a named one.
- `routeConfiguration()` with no id for a nameless one, which is the fallback for routes with no `routeConfigurationId`.
- XML `<routeConfiguration id="...">`; YAML `routeConfiguration` with `id`.

Assign: `routeConfigurationId` on the route. Give several ids separated by commas. Matching is by exact id (`"javaError"`), trailing wildcard (`"java*"`), or regex (`".*error.*"`).

Precedence: a route's own local error handler always wins; the configuration's handler is ignored. A route can have only one error handler.

Other details: add with `addRoutes`; Spring Boot discovers `@Component` ones. A `precondition` (simple expression evaluated once at startup) decides inclusion. Java, XML and YAML can be mixed. Setting `startup-summary-level` to verbose logs which configurations each route uses.

Verify: two routes with `routeConfigurationId("java*")` both use the matching configuration's onException.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel Route Configuration manual page. Confirmed: since Camel 3.12, the four strategies it holds, RouteConfigurationBuilder with configuration(), nameless fallback configuration, comma-separated ids, exact, wildcard and regex matching, local error handler always winning, addRoutes and Spring Boot @Component discovery, precondition evaluated once, mixing DSLs, startup-summary-level=verbose.
