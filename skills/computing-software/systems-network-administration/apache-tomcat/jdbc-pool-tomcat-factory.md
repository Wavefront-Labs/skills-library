---
id: computing-software.systems-network-administration.apache-tomcat.jdbc-pool-tomcat-factory
name: jdbc-pool-tomcat-factory
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, jdbc-pool, tomcat-jdbc, datasourcefactory, validationquery, testwhileidle, removeabandoned, jdbcinterceptors, connection-pool]
level: advanced
status: docs-checked
description: "Use the Tomcat JDBC pool (org.apache.tomcat.jdbc.pool) instead of DBCP: factory attribute, sizing and validation defaults, abandoned-connection handling, interceptors and JMX."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tomcat JDBC pool

Switch from the default pool by adding `factory` to the Resource:
```xml
<Resource name="jdbc/TestDB" auth="Container" type="javax.sql.DataSource"
          factory="org.apache.tomcat.jdbc.pool.DataSourceFactory"
          driverClassName="org.postgresql.Driver"
          url="jdbc:postgresql://127.0.0.1:5432/mydb"
          username="<DB_USER>" password="<DB_PASSWORD>"
          initialSize="10" maxActive="100" minIdle="10" maxWait="10000"
          testWhileIdle="true" testOnBorrow="true"
          validationQuery="SELECT 1" validationInterval="30000"
          timeBetweenEvictionRunsMillis="30000" minEvictableIdleTimeMillis="30000"
          removeAbandoned="true" removeAbandonedTimeout="60" logAbandoned="true"
          jdbcInterceptors="ConnectionState;StatementFinalizer"/>
```

| Attribute | Default |
|---|---|
| `initialSize` | 10 |
| `maxActive` | 100 |
| `maxIdle` | = maxActive |
| `minIdle` | from initialSize (10) |
| `maxWait` | 30000 ms |
| `testOnBorrow` / `testWhileIdle` | false / false (testWhileIdle must be true for the evictor) |
| `validationQuery` | null (uses `isValid()`) |
| `validationInterval` | 3000 ms |
| `timeBetweenEvictionRunsMillis` | 5000 (keep >= 1 s) |
| `minEvictableIdleTimeMillis` | 60000 |
| `removeAbandoned` / `removeAbandonedTimeout` | false / 60 s |
| `logAbandoned` | false (stack capture on each borrow costs) |
| `jdbcInterceptors` | null; bare names get the `org.apache.tomcat.jdbc.pool.interceptor.` prefix; options like `StatementFinalizer(useEquals=true)` |
| `defaultAutoCommit` | unset (driver default) |
| `jmxEnabled` | true |

Differences from DBCP2 names: `maxActive` not `maxTotal`, `maxWait` not `maxWaitMillis`.

Verify: JMX shows the pool MBean (`jmxEnabled` defaults to true).

## Checked

2026-11-04. Read the Tomcat 10.1 JDBC Connection Pool page (jdbc-pool.html): confirmed the factory class, every default in the table (initialSize, maxActive, maxIdle, minIdle, maxWait, test flags, validationQuery, validationInterval, eviction settings, removeAbandoned, logAbandoned, jdbcInterceptors prefix and option syntax, defaultAutoCommit, jmxEnabled) and the maxActive and maxWait naming. Removed the unsupported restart-the-database verification claim.

Method: documentation only; no commands were run.
