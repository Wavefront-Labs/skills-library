---
id: computing-software.systems-network-administration.apache-tomcat.jdbc-datasource-resource
name: jdbc-datasource-resource
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, jndi, datasource, jdbc, dbcp2, maxtotal, maxwaitmillis, resource, removeabandonedonborrow, resource-ref]
level: practitioner
status: docs-checked
description: "Define a JDBC DataSource in Tomcat 10.1 with a Context Resource using the default DBCP 2 pool: driver jar location, pool attributes, web.xml resource-ref and JNDI lookup."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/jndi-datasource-examples-howto.html
  - https://tomcat.apache.org/tomcat-10.1-doc/jndi-resources-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JDBC DataSource (DBCP 2 default)

1. Put the JDBC driver jar in `$CATALINA_HOME/lib`.
2. Declare in `META-INF/context.xml`:
```xml
<Context>
  <Resource name="jdbc/EmployeeDB" auth="Container" type="javax.sql.DataSource"
            driverClassName="org.postgresql.Driver"
            url="jdbc:postgresql://127.0.0.1:5432/mydb"
            username="<DB_USER>" password="<DB_PASSWORD>"
            maxTotal="20" maxIdle="10" maxWaitMillis="10000"/>
</Context>
```
3. Reference it in `WEB-INF/web.xml` (mind DTD element order):
```xml
<resource-ref>
  <res-ref-name>jdbc/EmployeeDB</res-ref-name>
  <res-type>javax.sql.DataSource</res-type>
  <res-auth>Container</res-auth>
</resource-ref>
```
4. Look up: `((DataSource) new InitialContext().lookup("java:/comp/env/jdbc/EmployeeDB")).getConnection()`; always close the connection to return it to the pool.

The howto sets `maxWaitMillis` to 10 seconds in its example and advises a 10-15 second connection timeout to ride out GC pauses. Tomcat's default pool is Commons DBCP 2 (repackaged in `tomcat-dbcp.jar`); for the full attribute list and its defaults see the DBCP 2 documentation, which this page defers to. Abandoned-connection defaults from the howto: `removeAbandonedOnBorrow` false, `removeAbandonedOnMaintenance` false, `removeAbandonedTimeout` 300 s, `logAbandoned` false.

Leak recovery: `removeAbandonedOnBorrow="true" removeAbandonedTimeout="60" logAbandoned="true"`; `removeAbandonedOnMaintenance` needs a positive `timeBetweenEvictionRunsMillis`.

Gotchas: Tomcat only uses `*.jar` files in `$CATALINA_HOME/lib`, so an old Oracle `.zip` driver must be renamed to `.jar`; the Oracle thin URL uses the SID, not the TNS name. A Resource in `GlobalNamingResources` is shared among the Contexts of the server; a Realm must refer to the datasource by its original name, not a `ResourceLink` rename.

Verify: a test servlet obtains a connection through the `java:/comp/env` lookup.

## Checked

2026-11-04. Read the Tomcat 10.1 JNDI Datasource How-To (jndi-datasource-examples-howto.html) and JNDI Resources How-To: confirmed driver jar placement in CATALINA_HOME/lib, the Resource and resource-ref examples, the lookup form, the abandoned-connection attributes and their defaults, the 10-15 second timeout advice, the Oracle jar rename and SID note, and the GlobalNamingResources and Realm notes. Removed the list of DBCP 2 pool defaults and the factory class name, which the pages do not state (they defer to the DBCP 2 documentation).

Method: documentation only; no commands were run.
