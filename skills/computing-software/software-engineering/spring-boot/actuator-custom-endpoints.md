---
id: computing-software.software-engineering.spring-boot.actuator-custom-endpoints
name: actuator-custom-endpoints
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, custom-endpoint, readoperation, writeoperation, selector, webendpoint]
level: practitioner
status: docs-checked
description: "Write custom Actuator endpoints with @Endpoint and read/write/delete operations: input mapping, HTTP method and status mapping, produces, selectors and security context."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `@Bean` annotated `@Endpoint` whose methods carry `@ReadOperation`, `@WriteOperation` or `@DeleteOperation` is exposed over JMX and, in a web app, HTTP (Jersey, Spring MVC or WebFlux; Spring MVC wins if both present). Technology-specific: `@JmxEndpoint`, `@WebEndpoint` (HTTP only). Extensions: `@EndpointWebExtension`, `@EndpointJmxExtension` (at most one of each type per endpoint). `@Controller`/`@RestController`/servlet endpoints give framework features but not JMX.

Input: web parameters come from query parameters and each root property of the JSON body; JMX maps to MBean operation parameters. Parameters are required unless annotated JSpecify `@Nullable` (Kotlin null safety also works). Only simple types in the signature (no single custom-data parameter). Compile with `-parameters` (automatic with Boot's Gradle plugin or Maven `spring-boot-starter-parent`). Conversion uses `ApplicationConversionService` plus `Converter`/`GenericConverter` beans qualified `@EndpointConverter`.

Web predicates:
- Path: `/actuator/<id>` (default base path); add path variables by annotating parameters with `@Selector`; `@Selector(Match=ALL_REMAINING)` on the last parameter (conversion-compatible with `String[]`) captures the rest.
- Method: read = `GET`, write = `POST`, delete = `DELETE`.
- Consumes: for a body-using `POST`, `application/vnd.spring-boot.actuator.v2+json, application/json`; otherwise empty.
- Produces: optional `produces` attribute; otherwise empty for `void`/`Void`, `application/octet-stream` for `Resource`, else `application/vnd.spring-boot.actuator.v2+json, application/json`.

Response status: read with value 200, without value 404; write or delete with value 200, without 204; missing or unconvertible parameter 400 (method not called).

Range requests: operations returning `Resource` support them under Spring MVC and WebFlux, not Jersey.

Security: an operation may take `java.security.Principal` (typically with `@Nullable`) or `SecurityContext` (use `isUserInRole(String)`) as a parameter.

## Checked

2026-11-07

Read endpoints.adoc (docs-repo source of the cited Actuator endpoints page) in full; used the Implementing Custom Endpoints section and its subsections (Receiving Input, Input Type Conversion, Custom Web Endpoints, request predicates: Path, HTTP method, Consumes, Produces, Response Status, Range Requests, Web Endpoint Security). The MyEndpoint include-code examples were not opened; claims rest on page prose.
Confirmed: @Endpoint with Read/Write/DeleteOperation exposed over JMX and HTTP; Jersey/MVC/WebFlux with MVC preferred; JmxEndpoint/WebEndpoint; EndpointWebExtension/EndpointJmxExtension with at most one of each type; parameter sources, required-by-default and JSpecify Nullable; simple-types-only tip; -parameters compile note; ApplicationConversionService and EndpointConverter; /actuator/<id> path, @Selector and ALL_REMAINING; GET/POST/DELETE mapping; consumes and produces values; 200/404/204/400 statuses; range requests unsupported with Jersey; Principal and SecurityContext.isUserInRole.
Nothing trimmed.

Method: documentation only; no commands were run.
