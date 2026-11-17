---
id: computing-software.systems-network-administration.zabbix.jmx-items
name: jmx-items
category: computing-software
field: systems-network-administration
product: zabbix
tags: [jmx, java-gateway, mbean, javagateway, startjavapollers]
level: practitioner
status: docs-checked
description: "Monitor Java applications over JMX through the Zabbix Java gateway with jmx[] items and composite attributes."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/jmx_monitoring
  - https://www.zabbix.com/documentation/current/en/manual/concepts/java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The server never talks JMX directly. It queries the Zabbix Java gateway, which uses the JMX management API against the application. Firewalls must not block the gateway-to-application path.

Server or proxy settings: JavaGateway (address), JavaGatewayPort (default 10052) and StartJavaPollers. Keep StartJavaPollers at or below StartPollers, otherwise the gateway may run out of threads for requests.

Enable remote JMX in the Java application with options such as -Dcom.sun.management.jmxremote, -Dcom.sun.management.jmxremote.port=12345, and authenticate and ssl set as needed. The bare-minimum example with authenticate=false and ssl=false listens on localhost only. To allow other interfaces set -Djava.rmi.server.hostname. For SSL, add the -Djavax.net.ssl.* options to the gateway startup script.

In the frontend, give the host a JMX interface and add JMX agent items. The key is jmx[object name,attribute name] , for example jmx["java.lang:type=Memory","HeapMemoryUsage.used"]. Composite attributes use dots: jmx[com.example:Type=Hello,fruits.apple.weight]. A tabular attribute returns the whole structure as JSON. Optional fields: custom JMX endpoint, user name and password (macros allowed).

For a Boolean counter use Numeric (unsigned) and the Boolean to decimal preprocessing step so true and false are stored as 1 and 0.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/jmx_monitoring; concepts/java): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
