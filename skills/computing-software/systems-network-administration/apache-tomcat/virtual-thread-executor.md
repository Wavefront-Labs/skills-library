---
id: computing-software.systems-network-administration.apache-tomcat.virtual-thread-executor
name: virtual-thread-executor
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, virtual-threads, standardvirtualthreadexecutor, usevirtualthreads, executor, java-21]
level: advanced
status: docs-checked
description: "Run Tomcat 10.1 request processing on Java 21 virtual threads using StandardVirtualThreadExecutor or the Connector useVirtualThreads attribute."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/executor.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Virtual thread request processing

Requires Java 21 or later.

Option 1, explicit Executor:
```xml
<Executor name="virtualThreads"
          className="org.apache.catalina.core.StandardVirtualThreadExecutor"
          namePrefix="app-virt-"/>
<Connector executor="virtualThreads" port="8080" protocol="HTTP/1.1"/>
```
- It starts a new virtual thread for every task.
- The documented attribute is `namePrefix` (default `tomcat-virt-`), plus the common `className` and `name`.

Option 2, Connector internal pool:
```xml
<Connector port="8080" protocol="HTTP/1.1" useVirtualThreads="true"/>
```
`useVirtualThreads` enables virtual threads with the connector's internal executor; it defaults to `false` and is ignored if an executor is associated with the connector.

Practical notes:
- Thread names are `namePrefix` plus the thread number.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Executor reference (Virtual Thread Implementation) and HTTP Connector reference (useVirtualThreads, executor). Removed the maxConnections default and concurrency claims and the generic verify line.

Method: documentation only; no commands were run.
