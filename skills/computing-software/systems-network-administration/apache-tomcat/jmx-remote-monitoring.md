---
id: computing-software.systems-network-administration.apache-tomcat.jmx-remote-monitoring
name: jmx-remote-monitoring
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, jmx, monitoring, remote-jmx, jmxremote, rmi-port, jmxremote-password, jmxproxyservlet, nagios]
level: advanced
status: docs-checked
description: "Enable secure remote JMX on Tomcat 10.1 via CATALINA_OPTS: jmxremote port and rmi.port, TLS, password and access files, hostname binding, and the HTTP JMXProxyServlet alternative."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remote JMX

Only needed for remote monitoring; local tools under the same OS user work without it. Put options in `bin/setenv.sh` (or `setenv.bat`) as `CATALINA_OPTS`.

Minimal (lab only):
```
-Dcom.sun.management.jmxremote.port=<JMX_PORT>
-Dcom.sun.management.jmxremote.rmi.port=<RMI_PORT>
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.authenticate=false
```
Set `rmi.port` explicitly; otherwise the RMI port is chosen at random, which makes a firewall hard to configure.

Production: TLS plus auth.
```
-Dcom.sun.management.jmxremote.ssl=true
-Dcom.sun.management.jmxremote.registry.ssl=true
-Dcom.sun.management.jmxremote.ssl.need.client.auth=true
-Dcom.sun.management.jmxremote.authenticate=true
-Dcom.sun.management.jmxremote.password.file=../conf/jmxremote.password
-Dcom.sun.management.jmxremote.access.file=../conf/jmxremote.access
```
(also `...ssl.enabled.protocols` and `...ssl.enabled.cipher.suites`; JAAS via `...login.config`.)

`conf/jmxremote.access`: `monitorRole readonly` / `controlRole readwrite`. `conf/jmxremote.password`: `monitorRole <PASSWORD>`; make the password file read-only and accessible only by the OS user Tomcat runs as.

Bind/advertise: `-Dcom.sun.management.jmxremote.host=<bind-interface>` and `-Djava.rmi.server.hostname=<public-host>` (RMI stubs carry this address).

Alternative: the JMXProxyServlet exposes JMX over HTTP, so monitoring tools like Nagios make one HTTP call per datum instead of starting a JVM per check. The page defers its syntax to the Manager documentation.

Verify: a remote JMX client connects to `<JMX_PORT>` with the configured credentials.

## Checked

2026-11-04. Read the Tomcat 10.1 Monitoring and Managing Tomcat page (monitoring.html): confirmed the jmxremote port, rmi.port, ssl, registry.ssl, protocol, cipher and client-auth options, authenticate with the password and access files and their sample roles, the JAAS login.config option, java.rmi.server.hostname, jmxremote.host and the JMXProxyServlet advantages. Removed the manager-jmx role (not on this page), the sample-password advice, and the jconsole and firewall verify detail.

Method: documentation only; no commands were run.
