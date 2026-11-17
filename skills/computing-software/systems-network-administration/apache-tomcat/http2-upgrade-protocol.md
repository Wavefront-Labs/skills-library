---
id: computing-software.systems-network-administration.apache-tomcat.http2-upgrade-protocol
name: http2-upgrade-protocol
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, http2, upgradeprotocol, http2protocol, maxconcurrentstreams, h2c, overheadcountfactor, stream-timeouts]
level: advanced
status: docs-checked
description: "Enable HTTP/2 in Tomcat 10.1 by nesting UpgradeProtocol Http2Protocol in a Connector and tune maxConcurrentStreams, timeouts, window size and overhead protection."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http2.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP/2

Nest inside an HTTP/1.1 Connector (TLS `h2`, upgrade `h2c`, or prior-knowledge `h2c`):
```xml
<Connector port="8443" protocol="HTTP/1.1" SSLEnabled="true">
  <UpgradeProtocol className="org.apache.coyote.http2.Http2Protocol"
                   maxConcurrentStreams="100"/>
  <SSLHostConfig>...</SSLHostConfig>
</Connector>
```

Defaults on `Http2Protocol`:

| Attribute | Default |
|---|---|
| `maxConcurrentStreams` | 100 (extra streams get STREAM_REFUSED) |
| `maxConcurrentStreamExecution` | 20 (container threads per connection) |
| `initialWindowSize` | 65535 |
| `keepAliveTimeout` | 20000 ms |
| `readTimeout` / `writeTimeout` | 5000 ms |
| `streamReadTimeout` / `streamWriteTimeout` | 20000 ms |
| `maxHeaderCount` / `maxTrailerCount` | 100 |
| `overheadCountFactor` | 10 (<1 disables the protection) |
| `overheadResetFactor` | 50 |
| `overheadContinuationThreshold` / `overheadDataThreshold` / `overheadWindowUpdateThreshold` | 1024 |
| `allowSchemeMismatch` | false; true only behind a trusted TLS-terminating proxy |
| `useSendfile` | true (ignored if Connector `useAsyncIO` is false) |
| `drainTimeout` | 0 ns |

Header size limits come from the Connector (`maxHttpHeaderSize`, `maxTrailerSize`), not Http2Protocol. The overhead attributes close connections that generate too many overhead frames; do not disable them casually.

Verify: `curl --http2 -I https://host:8443/` reports `HTTP/2 200`.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP2 Upgrade Protocol page (config/http2.html) and HTTP Connector page: confirmed every Http2Protocol attribute and default in the table, the nesting inside an HTTP/1.1 Connector, the inherited maxHttpHeaderSize and maxTrailerSize, and the useSendfile and useAsyncIO link. Reworded the rapid-reset remark to what the page describes.

Method: documentation only; no commands were run.
