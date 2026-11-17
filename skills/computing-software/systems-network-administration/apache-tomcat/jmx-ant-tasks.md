---
id: computing-software.systems-network-administration.apache-tomcat.jmx-ant-tasks
name: jmx-ant-tasks
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, jmx, ant, jmx-open, jmx-get, jmx-set, jmx-invoke, jmx-query, mbean, catalina-ant]
level: advanced
status: docs-checked
description: "Script Tomcat 10.1 JMX from Ant: open a connection, get/set attributes, invoke operations, query MBeans and wait on conditions using catalina-ant.jar and catalina-tasks.xml."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JMX Ant tasks

Setup: copy `catalina-ant.jar` from `$CATALINA_HOME/lib` to `$ANT_HOME/lib`; `<import file="${CATALINA.HOME}/bin/catalina-tasks.xml"/>`; enable remote JMX first (`computing-software.systems-network-administration.apache-tomcat.jmx-remote-monitoring`).

```xml
<jmx:open host="${jmx.server.name}" port="${jmx.server.port}"
          username="controlRole" password="<PASSWORD>"/>

<jmx:get name="Catalina:type=Manager,context=/myapp,host=localhost"
         attribute="maxActiveSessions" resultproperty="old.max" echo="true"/>

<jmx:set name="Catalina:type=Manager,context=/myapp,host=localhost"
         attribute="maxActiveSessions" value="100" type="int"/>

<jmx:invoke name="Catalina:type=Manager,context=/myapp,host=localhost"
            operation="listSessionIds" resultproperty="sessions"
            delimiter=" " echo="false"/>

<jmx:query name="Catalina:type=Manager,*" resultproperty="manager"
           attributebinding="true" echo="true"/>
```

Wait for a condition (for example a cluster sender connected):
```xml
<jmx:condition operation="==" host="localhost" port="9014"
   username="controlRole" password="<PASSWORD>"
   name="Catalina:type=IDataSender,host=localhost,senderAddress=192.168.111.1,senderPort=9025"
   attribute="connected" value="true"/>
```
The `name` must be one line with no spaces.

MBeans the page names: `Catalina:type=Manager,...` (`maxActiveSessions`, `activeSessions`, `listSessionIds`), `IDataSender` (`connected`), `ClusterSender`, `Cluster`, `MBeanFactory` (`createAccessLoggerValve`).

Verify: the `echo="true"` get prints the current value.

## Checked

2026-11-04. Read the Tomcat 10.1 Monitoring and Managing Tomcat page (monitoring.html): confirmed the catalina-ant.jar copy to ANT_HOME/lib, the catalina-tasks.xml import, the open, get, set, invoke and query attributes and examples, the jmx:condition attributes and the IDataSender wait example, the one-line name note and the MBean names used. Nothing removed.

Method: documentation only; no commands were run.
