---
id: computing-software.systems-network-administration.apache-tomcat.http-connector-request-limits
name: http-connector-request-limits
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, http-connector, request-limits, maxpostsize, maxparametercount, maxhttpheadersize, maxswallowsize, multipart-limits]
level: practitioner
status: docs-checked
description: "Tomcat 10.1 HTTP Connector request limit attributes: maxParameterCount, maxPartCount, maxPostSize, header size and count limits, maxSwallowSize, defaults and memory impact."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP Connector request limits

Goal: cap request size and parsing work per `<Connector>`.

| Attribute | Default | Notes |
|---|---|---|
| `maxParameterCount` | 10000 | Query + form + upload parameters; <0 = no limit. `FailedRequestFilter` can reject excess |
| `maxPartCount` | 50 | Multipart parts |
| `maxPartHeaderSize` | 512 bytes | Per part |
| `maxPostSize` | 2097152 | Only form body bytes parsed into parameters; <0 disables |
| `maxSavePostSize` | 4096 | Body saved during FORM/CLIENT-CERT auth or HTTP/1.1 upgrade; -1 unlimited, 0 off |
| `maxHttpHeaderSize` | 8192 | Default for request and response header limits |
| `maxHttpRequestHeaderSize` / `maxHttpResponseHeaderSize` | = `maxHttpHeaderSize` | Set separately if needed |
| `maxHeaderCount` | 100 | <0 = no limit |
| `maxCookieCount` | 200 | |
| `maxSwallowSize` | 2097152 | Bytes drained from an aborted upload; <0 = no limit |
| `maxTrailerSize` | 8192 | Chunked trailer headers |
| `allowedTrailerHeaders` | empty | Trailers are ignored unless listed |
| `rejectIllegalHeader` | true | false ignores bad headers |

Memory warnings from the page:
- Multipart worst case is `maxPartHeaderSize x maxPartCount x maxConnections x 2`, about 400 MB with defaults.
- Header buffers are allocated in full per request: 1 MB limit x 100 concurrent requests = 100 MB heap.

Example (stricter headers):
```xml
<Connector port="8080" protocol="HTTP/1.1" maxHttpHeaderSize="8192"
           maxParameterCount="1000" maxPartCount="20" maxSwallowSize="1048576"/>
```

Verify: send an oversized header with curl; expect a 400 or connection close.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html) and confirmed every attribute, default and the multipart memory formula (about 400MB with defaults) and the 1 MB x 100 requests header example. Nothing removed.

Method: documentation only; no commands were run.
