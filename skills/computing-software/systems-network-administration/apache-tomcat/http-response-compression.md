---
id: computing-software.systems-network-administration.apache-tomcat.http-response-compression
name: http-response-compression
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, http-connector, compression, gzip, compressionminsize, compressiblemimetype, nocompressionuseragents, sendfile]
level: practitioner
status: docs-checked
description: "Enable gzip response compression on a Tomcat 10.1 HTTP Connector: compression modes, compressionMinSize, compressibleMimeType, user-agent exclusions and the sendfile conflict."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP response compression

Set on the `<Connector>`:

| Attribute | Default | Notes |
|---|---|---|
| `compression` | off | `off`, `on`, `force`, or an integer minimum size in bytes (same as `on`) |
| `compressionMinSize` | 2048 | Minimum response size when `compression="on"` |
| `compressibleMimeType` | text/html, text/xml, text/plain, text/css, text/javascript, application/javascript, application/json, application/xml | Setting it replaces the whole list |
| `noCompressionUserAgents` | empty | Regex matched against the full User-Agent |

Behaviour:
- `on` also compresses responses of unknown length.
- Compression is skipped if the response already carries a Content-Encoding the Connector treats as compressed (the page's default list includes br, compress, dcb, dcz, deflate, gzip and zstd).
- With NIO, `useSendfile` (default true) wins over compression: static files above 48 KiB go out uncompressed. Set `useSendfile="false"` on the Connector, or change the DefaultServlet sendfile threshold, if you need them compressed.

Example:
```xml
<Connector port="8080" protocol="HTTP/1.1" compression="on"
           compressionMinSize="1024"
           compressibleMimeType="text/html,text/css,application/json,application/javascript"/>
```

Verify: `curl -s -H "Accept-Encoding: gzip" -D - -o /dev/null http://localhost:8080/app/big.json` shows `Content-Encoding: gzip`.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html) and confirmed compression modes, compressionMinSize 2048, the default compressibleMimeType list, noCompressionUserAgents, the useSendfile and 48 KiB conflict and the already-compressed encoding list. Removed the pack200-gzip name because the page text spells it differently.

Method: documentation only; no commands were run.
