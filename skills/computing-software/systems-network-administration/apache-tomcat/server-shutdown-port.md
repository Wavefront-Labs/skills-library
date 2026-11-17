---
id: computing-software.systems-network-administration.apache-tomcat.server-shutdown-port
name: server-shutdown-port
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, server-element, shutdown-port, portoffset, utilitythreads, server-xml]
level: practitioner
status: docs-checked
description: "Configure the Tomcat 10.1 Server element: shutdown port and command, address, portOffset for side-by-side instances, utilityThreads and periodicEventDelay."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/server.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server element: shutdown port, portOffset, utility threads

`<Server>` is the root of `conf/server.xml`.

| Attribute | Default | Meaning |
|---|---|---|
| `port` | set in `server.xml` | Shutdown listener port; -1 disables it |
| `shutdown` | set in `server.xml` | Command string that stops Tomcat |
| `address` | localhost | Listener address |
| `portOffset` | 0 | Added to `port` and every nested connector port (non-negative) |
| `utilityThreads` | 1 | Threads for background tasks; 0 = CPU count; negative = CPU count + value, min 1 |
| `utilityThreadsAsDaemon` | false | StandardServer only |
| `periodicEventDelay` | 10 s | Interval for periodic lifecycle events; <=0 disables |

Notes:
- `port="-1"` works with Apache Commons Daemon (Windows service, jsvc) but breaks `shutdown.sh/.bat` and `catalina.sh stop`, which cannot then stop Tomcat gracefully.
- Change the `shutdown` string from the default, or disable the port, on shared hosts; anyone who can reach the port with the string can stop the server.
- `portOffset="100"` turns 8080 into 8180 and 8005 into 8105, a quick way to run several instances from one config.

```xml
<Server port="8005" shutdown="<RANDOM_STRING>" portOffset="100">
```

Verify: `ss -ltn` (or `netstat -an`) shows the shifted ports after restart.

## Checked

2026-11-04. Read the Tomcat 10.1 Server page (config/server.html): confirmed address default localhost, port -1 and its Commons Daemon caveat, portOffset, utilityThreads, utilityThreadsAsDaemon and periodicEventDelay. Removed the stock-file values 8005 and SHUTDOWN from the table because the page gives no defaults for them (the example still uses 8005 as a sample value).

Method: documentation only; no commands were run.
