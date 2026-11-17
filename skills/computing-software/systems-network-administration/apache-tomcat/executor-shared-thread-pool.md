---
id: computing-software.systems-network-administration.apache-tomcat.executor-shared-thread-pool
name: executor-shared-thread-pool
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, executor, standardthreadexecutor, thread-pool, maxqueuesize, minsparethreads, threadrenewaldelay]
level: practitioner
status: docs-checked
description: "Define a shared Tomcat 10.1 Executor thread pool in server.xml, its StandardThreadExecutor attributes and defaults, and reference it from Connectors."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/executor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shared Executor thread pool

An `<Executor>` is a child of `<Service>` and must appear before any Connector that uses it.

StandardThreadExecutor (default `className`):

| Attribute | Default |
|---|---|
| `name` | required, unique |
| `namePrefix` | `tomcat-exec-` |
| `maxThreads` | 200 |
| `minSpareThreads` | 25 |
| `maxIdleTime` | 60000 ms |
| `maxQueueSize` | Integer.MAX_VALUE |
| `threadPriority` | 5 |
| `daemon` | true |
| `threadRenewalDelay` | 1000 ms (negative disables) |

`threadRenewalDelay` works with `ThreadLocalLeakPreventionListener`: after a context stops, pool threads are renewed, with this delay between renewals.

```xml
<Service name="Catalina">
  <Executor name="tomcatThreadPool" namePrefix="catalina-exec-"
            maxThreads="150" minSpareThreads="4" maxQueueSize="1000"/>
  <Connector executor="tomcatThreadPool" port="8080"
             protocol="HTTP/1.1" connectionTimeout="20000" redirectPort="8443"/>
</Service>
```

When a Connector has `executor`, its own `maxThreads`, `minSpareThreads`, `threadPriority`, `threadsMaxIdleTime`, `useVirtualThreads` are ignored. A bounded `maxQueueSize` makes overflow tasks get rejected instead of queuing without limit.

Verify: `jstack` or a thread dump shows threads named `catalina-exec-N`.

## Checked

2026-11-04. Read the Tomcat 10.1 Executor page (config/executor.html) and HTTP Connector page: confirmed the className default, every StandardThreadExecutor attribute default, the Executor-before-Connector ordering rule, threadRenewalDelay behaviour and the Connector attributes ignored when an executor is set. Nothing removed.

Method: documentation only; no commands were run.
