---
id: computing-software.messaging-and-integration.apache-camel.http-component
name: http-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, http, client, producer, headers]
level: practitioner
status: docs-checked
description: "Camel http producer: method selection order, CamelHttp headers, throwExceptionOnFailure true, bridgeEndpoint, connection pool 20 per route and 200 total, and timeout defaults."
sources:
  - https://camel.apache.org/components/next/http-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http: (client)

Producer only: `http:hostname[:port][/resourceUri][?options]`; default ports 80 and 443; artifact `camel-http`.

Method choice, in order: endpoint `httpMethod` (header cannot override), header `CamelHttpMethod`, GET if a query string is in `CamelHttpQuery`/`CamelHttpUri`/the URI, POST if there is a body, else GET. A body anywhere turns a call into POST, so set `httpMethod=GET` explicitly.

Headers: `CamelHttpResponseCode`, `CamelHttpResponseText`, `CamelHttpQuery` (overrides endpoint params), `CamelHttpUri` (overrides endpoint URI, ignored when `bridgeEndpoint=true`), `CamelHttpPath`.

Failure: `throwExceptionOnFailure` true. 100-299 succeed; 300-399 and 400+ throw `HttpOperationFailedException` (status code, redirect location, body). Set false to receive every response. `okStatusCodeRange` `200-299`.

Defaults: `bridgeEndpoint` false, `copyHeaders` true, `followRedirects` false, `connectionClose` false, `ignoreResponseBody` false, `getWithBody`/`deleteWithBody` false, `authenticationPreemptive` false (enable for basic auth with streamed bodies to avoid `NonRepeatableRequestException`).

Pool: `connectionsPerRoute` 20, `maxTotalConnections` 200.

Timeouts (component): `connectionRequestTimeout`, `connectTimeout`, `soTimeout` all 180000 ms; `responseTimeout` unset (0 is infinite). `responsePayloadStreamingThreshold` 8192 bytes. `automaticRetriesDisabled` false (disable to avoid long waits on 429 with large Retry-After).

Verify: a 404 reply throws `HttpOperationFailedException` unless `throwExceptionOnFailure=false`.

## Checked

Method: docs-checked 2026-11-09 against the camel.apache.org http-component page (component and endpoint options, message headers, method selection, response code handling, 429 retry and preemptive auth sections).
