---
id: computing-software.messaging-and-integration.apache-camel.to-dynamic
name: to-dynamic
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, tod, dynamic-endpoint, optimised-components]
level: practitioner
status: docs-checked
description: "Camel toD EIP: dynamic endpoint URIs with Simple, cacheSize and allowedSchemes, optimised components that reuse one producer, and the endpoint cache growth trap."
sources:
  - https://camel.apache.org/components/next/eips/toD-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# toD

Sends to an endpoint evaluated per message (`to` is static). The URI uses Simple by default; `pattern` can set InOnly or InOut.

```java
toD("${header.foo}")
toD("mock:${header.foo}")
toD("language:xpath:/order/@uri")
```
Without the `language:` prefix the value is a component name.

Options: `cacheSize` (0 default, -1 off), `allowOptimisedComponents` true, `autoStartComponents` true, `ignoreInvalidEndpoint` false, `allowedSchemes` unset (when set, other schemes are rejected regardless of `ignoreInvalidEndpoint`), `variableSend`, `variableReceive`. Property `CamelToEndpoint`.

Trap: varying parameters (a `userid` per user) create one endpoint and producer per value. `cacheSize` (say 10) trims the cache but does not stop endpoint creation; prefer a static `to` with dynamic values in headers.

Optimised components: the component name must be static (or a property placeholder) and the supported component on the classpath. HTTP ones: camel-http, jetty, netty-http, undertow, vertx-http; others include activemq, amqp, file, ftp, jms, kafka, paho-mqtt5. The dynamic parts move into `CamelHttpPath` and `CamelHttpQuery`, the URI becomes static and one producer is reused. When optimised you cannot override with `Exchange.HTTP_PATH` or `HTTP_QUERY`; use plain `to`.

Debug: DEBUG on `org.apache.camel.processor.SendDynamicProcessor` shows whether optimisation happened.

Verify: `toD("mock:${header.foo}")` with foo=order delivers to `mock:order`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel toD EIP page: option list and defaults, Simple evaluation, pattern InOnly or InOut, the language: prefix rule, the endpoint cache growth warning and cacheSize caveat, the lists of optimised HTTP and non-HTTP components, the three conditions for optimisation, the HTTP_PATH and HTTP_QUERY override restriction, the SendDynamicProcessor DEBUG hint and allowedSchemes behaviour all match. No commands were run.
