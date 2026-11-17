---
id: computing-software.systems-network-administration.apache-tomcat.http-connector-threads-and-connections
name: http-connector-threads-and-connections
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, http-connector, connector, maxthreads, acceptcount, maxconnections, connectiontimeout, keepalive, thread-pool]
level: practitioner
status: docs-checked
description: "Size a Tomcat 10.1 HTTP Connector: maxThreads, minSpareThreads, acceptCount, maxConnections, connectionTimeout and keep-alive attributes, their defaults and how they interact."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP Connector threads and connections

Goal: set concurrency and timeouts on a `<Connector>` in `conf/server.xml`.

| Attribute | Default | Meaning |
|---|---|---|
| `maxThreads` | 200 | Request processing threads |
| `minSpareThreads` | 10 | Threads kept alive (active + idle) |
| `threadsMaxIdleTime` | 60000 ms | Idle time before extra threads stop |
| `maxConnections` | 8192 | Connections accepted and processed at once; -1 disables counting (NIO/NIO2) |
| `acceptCount` | 100 | OS accept queue length once `maxConnections` is hit (the OS may ignore it) |
| `connectionTimeout` | 60000 ms in code; 20000 in shipped `server.xml` | Wait for the request line; -1 = infinite |
| `keepAliveTimeout` | = `connectionTimeout` | Wait for the next request |
| `maxKeepAliveRequests` | 100 | 1 disables keep-alive and pipelining; -1 unlimited |
| `processorCache` | 200 | -1 unlimited, 0 no reuse |

Notes:
- If the Connector has an `executor` attribute, `maxThreads`, `minSpareThreads`, `threadPriority` and `threadsMaxIdleTime` are ignored; set them on the Executor (see `computing-software.systems-network-administration.apache-tomcat.executor-shared-thread-pool`).
- Upload timeout: `disableUploadTimeout` is `true` by default; set `false` to use `connectionUploadTimeout` (300000 ms).
- For non-async apps set `processorCache` near `maxThreads`; with async servlets use the larger of `maxThreads` and expected concurrent requests.
- `bindOnInit` (true) binds the port at init; `false` binds at start.

Example:
```xml
<Connector port="8080" protocol="HTTP/1.1" maxThreads="400"
           acceptCount="100" connectionTimeout="20000" redirectPort="8443"/>
```

Verify: after restart, check the connector thread count over JMX.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html) and confirmed the defaults for maxThreads, minSpareThreads, threadsMaxIdleTime, maxConnections, acceptCount, connectionTimeout (60000 in code, 20000 in shipped server.xml), keepAliveTimeout, maxKeepAliveRequests, processorCache, disableUploadTimeout, connectionUploadTimeout, bindOnInit and the executor override. Removed the unsupported Manager status and catalina.out warning claims.

Method: documentation only; no commands were run.
