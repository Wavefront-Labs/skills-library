---
id: computing-software.systems-network-administration.apache-tomcat.default-servlet-sendfile-precompressed
name: default-servlet-sendfile-precompressed
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, default-servlet, sendfile, sendfilesize, precompressed, brotli, gzip, static-content, buffers]
level: advanced
status: docs-checked
description: "Serve static files efficiently from Tomcat 10.1 DefaultServlet: sendfileSize threshold, precompressed .br/.gz variants, input/output buffers, and connector compression."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/default-servlet.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Static content: sendfile and precompressed files

DefaultServlet init-params:

| Param | Default | Notes |
|---|---|---|
| `sendfileSize` | 48 (KiB) | Minimum file size for sendfile; negative disables |
| `precompressed` | false | Serve existing compressed siblings when the client accepts them |
| `input` / `output` | 2048 bytes | Buffer sizes |
| `useAcceptRanges` | true | Deprecated; hard-coded true in Tomcat 12 |

`precompressed` accepts `true` or a mapping list:
```xml
<init-param>
  <param-name>precompressed</param-name>
  <param-value>br=.br,gzip=.gz</param-value>
</init-param>
```
Put `app.js`, `app.js.br`, `app.js.gz` side by side; the servlet picks by `Accept-Encoding`.

Interaction with Connector compression (see `computing-software.systems-network-administration.apache-tomcat.http-response-compression`): with NIO, sendfile takes precedence, so static files above 48 KiB go out uncompressed by the on-the-fly compressor. Choose one: precompress at build time (good, no CPU per request), set `useSendfile="false"` on the Connector, or raise `sendfileSize` so that files stay on the compression path.

Put overrides in `WEB-INF/tomcat-web.xml` (per app) or `conf/web.xml` (global).

Verify: `curl -s -H "Accept-Encoding: br" -D - -o /dev/null http://localhost:8080/app/app.js` shows `Content-Encoding: br`.

## Checked

2026-11-04. Read the Tomcat 10.1 Default Servlet page (default-servlet.html) and HTTP Connector page (config/http.html): confirmed sendfileSize 48 KiB with negative disabling, precompressed default false and the encoding=extension list syntax, input and output 2048, useAcceptRanges deprecated, tomcat-web.xml and conf/web.xml override locations, and the sendfile-over-compression note. Nothing removed.

Method: documentation only; no commands were run.
