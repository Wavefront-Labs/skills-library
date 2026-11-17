---
id: computing-software.messaging-and-integration.apache-camel.rest-dsl-basics
name: rest-dsl-basics
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, rest-dsl, http-status, inline-routes, platform-http]
level: intro
status: docs-checked
description: "Camel Rest DSL basics: rest() verbs mapped to direct routes, path parameters as headers, default 200/204 status, CamelHttpResponseCode, disabled() and inlineRoutes."
sources:
  - https://camel.apache.org/manual/rest-dsl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rest DSL basics

The Rest DSL is a facade that builds REST consumers for routes. It needs `camel-rest` plus a transport component: netty-http, jetty, platform-http (recommended), servlet or undertow.

```java
rest("/stock").get("/{sku}").to("direct:one-sku");
```

- `rest("/say")` sets a base path; verbs (`get`, `post`, `delete`) add URI templates. Duplicate slashes are removed.
- Path parameters like `{id}` arrive as headers of the same name.
- `.consumes("application/json")` restricts content type; `.to("direct:name")` hands off to a route.
- `.disabled()` or `.disabled("{{ordersEnabled}}")` turns an endpoint off (`disabled` attribute in XML, key in YAML).

Status codes: 200 by default, 204 with no body. Set header `CamelHttpResponseCode` (`Exchange.HTTP_RESPONSE_CODE`) to change it. Unhandled exceptions give 500; use `onException` for a specific status.

`restConfiguration().inlineRoutes(true)` (property `camel.rest.inline-routes`) inlines the linked `direct` route. It is enabled by default from Camel 4.5, off in 4.4 and older. Each REST endpoint needs its own unique `direct` endpoint; a direct route shared by several endpoints is not inlined and inlined routes cannot be called from other routes.

Each service is a route, so JMX can start or stop it, and a Rest Registry MBean lists services. Contract-first OpenAPI is available from Camel 4.6.

Verify: in the page's `/stock/{sku}` example, the otherwise branch sets `CamelHttpResponseCode` to 404 and a body naming the unknown SKU.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Rest DSL manual page: the supported components list (platform-http recommended), base path and duplicate slash handling, path parameters as headers, consumes, disabled in Java, XML and YAML, the 200 or 204 default, CamelHttpResponseCode, 500 on unhandled exceptions, inline-routes defaults (off in 4.4 and older, on from 4.5), the unique 1:1 direct rule, camel.rest.inline-routes, route-per-service JMX management, the Rest Registry MBean and the 4.6 contract-first note all match. The verify line was reworded to the page's example. No commands were run.
