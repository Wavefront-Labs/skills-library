---
id: computing-software.systems-network-administration.apache-tomcat.http-connector-uri-encoding
name: http-connector-uri-encoding
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, http-connector, uri-encoding, uriencoding, encodedsolidushandling, relaxedpathchars, allowbackslash, rejectsuspicioususris]
level: advanced
status: docs-checked
description: "Control how a Tomcat 10.1 HTTP Connector decodes URIs: URIEncoding, encoded slash handling, backslash, relaxedPathChars/relaxedQueryChars and rejectSuspiciousURIs."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# URI encoding and path character handling

Goal: decide which odd URIs the Connector accepts.

| Attribute | Default | Notes |
|---|---|---|
| `URIEncoding` | UTF-8 | Charset applied after `%xx` decoding |
| `useBodyEncodingForURI` | false | Use the encoding from contentType for query parameters instead of `URIEncoding` (query string only, not the path) |
| `encodedSolidusHandling` | reject | `%2f`: `reject` (400), `decode`, `passthrough` |
| `encodedReverseSolidusHandling` | decode | `%5c`: `reject` (400), `decode` (to `\`, then `allowBackslash` applies), `passthrough` |
| `allowBackslash` | false | Treat `\` as a path delimiter |
| `relaxedPathChars` | none | Extra characters allowed in the path |
| `relaxedQueryChars` | none | Same, for the query string |
| `rejectSuspiciousURIs` | false | Rejects requests whose URI matches the suspicious URI patterns identified by the Servlet 6.0 specification |

Valid relaxed characters are only: `" < > [ \ ] ^ ` { | }`. Anything else is ignored.

Example for an app that sends brackets and pipes in query strings (list only characters you really see):
```xml
<Connector port="8080" protocol="HTTP/1.1" relaxedQueryChars="[]|"/>
```

With `passthrough` for `%2f` or `%5c`, the application is responsible for any further `%nn` decoding; `%25` sequences are also left unchanged.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 HTTP Connector reference: attribute names, defaults, relaxed character list. Removed unsupported security rationale and the generic verify line.

Method: documentation only; no commands were run.
